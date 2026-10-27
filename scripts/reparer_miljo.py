"""Gendanner pakker i .venv, hvis filer er erstattet af en karantænetekst.

En sikkerhedstjeneste på maskinen erstatter af og til en fil i .venv (fx
django/utils/cache.py) med en tekstfil (cache.py.txt), som begynder med en besked om
karantæne. Så kan Django ikke starte. Scriptet finder sådanne filer og geninstallerer
den pakke, de hører til, i samme udgave. Det omgår ikke sikkerhedstjenesten og rører
ikke karantænefilerne.

Kun Pythons standardbibliotek bruges, så scriptet virker, selv når Django er i stykker.

Kør fra projektmappen:

    .venv\\Scripts\\python.exe scripts\\reparer_miljo.py          (gendan)
    .venv\\Scripts\\python.exe scripts\\reparer_miljo.py --tjek   (kun tjek, ændrer intet)

Returkoder: 0 i orden, 1 tjek fandt karantænefiler, 2 fejl (gendannelsen eller kontrollen
mislykkedes, eller en pakke kunne ikke bestemmes).
"""

import argparse
import csv
import os
import re
import subprocess
import sys
from email.parser import BytesParser
from pathlib import Path

QUARANTINE_MESSAGE = "This file is quarantined all because it triggered Web Reputation."
QUARANTINE_SUFFIX = ".py.txt"
IMPORT_CHECK = "import django, django.utils.cache"

EXIT_OK = 0
EXIT_FOUND = 1
EXIT_ERROR = 2

_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_VERSION_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+!-]*$")


class Package:
    """En installeret pakke: navn og udgave fra installationsoplysningerne."""

    def __init__(self, name, version):
        self.name = name
        self.version = version

    def __eq__(self, other):
        return (self.name, self.version) == (other.name, other.version)

    def __hash__(self):
        return hash((self.name, self.version))

    def __repr__(self):
        return f"Package({self.name!r}, {self.version!r})"


def project_root():
    """Projektroden er mappen over scripts/, uanset hvor kommandoen køres fra."""
    return Path(__file__).resolve().parent.parent


def find_venv_python(venv):
    """Fortolkeren i miljøet (Windows først, ellers Linux/macOS)."""
    for candidate in (venv / "Scripts" / "python.exe", venv / "bin" / "python"):
        if candidate.exists():
            return candidate
    return None


def find_site_packages(venv):
    """Pakkemappen i miljøet, eller None."""
    windows = venv / "Lib" / "site-packages"
    if windows.is_dir():
        return windows
    for candidate in sorted((venv / "lib").glob("python*/site-packages")):
        if candidate.is_dir():
            return candidate
    return None


def is_quarantine_file(path):
    """Sandt, hvis filens første bytes er karantænebeskeden. Læser kun starten."""
    try:
        with open(path, "rb") as handle:
            start = handle.read(512)
    except OSError:
        return False
    if start.startswith(b"\xef\xbb\xbf"):
        text = start[3:].decode("utf-8", errors="replace")
    elif start.startswith((b"\xff\xfe", b"\xfe\xff")):
        text = start.decode("utf-16", errors="replace")
    else:
        text = start.decode("utf-8", errors="replace")
    return text.lstrip().startswith(QUARANTINE_MESSAGE)


def find_quarantine_files(site_packages):
    """Karantænefiler under pakkemappen, hvis originale fil mangler.

    Har en tidligere reparation gendannet pakken, ligger den gamle karantænefil stadig,
    men den originale .py er tilbage. Så er filen ikke et nyt fund.
    """
    found = []
    for folder, _dirs, files in os.walk(site_packages):
        for name in files:
            if not name.endswith(QUARANTINE_SUFFIX):
                continue
            path = Path(folder) / name
            original = path.with_name(name[: -len(".txt")])
            if original.exists():
                continue
            if is_quarantine_file(path):
                found.append(path)
    return sorted(found)


def _read_metadata(dist_info):
    """Navn og udgave fra METADATA, eller None."""
    try:
        with open(dist_info / "METADATA", "rb") as handle:
            headers = BytesParser().parse(handle, headersonly=True)
    except OSError:
        return None
    name, version = headers.get("Name"), headers.get("Version")
    if not name or not version:
        return None
    name, version = name.strip(), version.strip()
    if not _NAME_RE.match(name) or not _VERSION_RE.match(version):
        return None
    return Package(name, version)


def _top_level_name(relative):
    """Første led i en sti fra RECORD; et modul i roden mister sin .py."""
    parts = relative.replace("\\", "/").split("/")
    first = parts[0]
    if first in ("", "..", ".") or first.endswith((".dist-info", ".data")):
        return None
    if len(parts) == 1 and first.endswith(".py"):
        first = first[:-3]
    return first


def build_indexes(site_packages):
    """Slår filer og topniveau-navne op til pakker via dist-info-mapperne.

    Returnerer (filer, topniveau): filer er sti i RECORD -> pakke, topniveau er
    øverste mappe eller modul -> pakke (fra top_level.txt, ellers RECORD).
    """
    by_file = {}
    by_top = {}
    for dist_info in sorted(Path(site_packages).glob("*.dist-info")):
        package = _read_metadata(dist_info)
        if package is None:
            continue
        top_names = set()
        top_file = dist_info / "top_level.txt"
        if top_file.is_file():
            for line in top_file.read_text(encoding="utf-8", errors="replace").splitlines():
                if line.strip():
                    top_names.add(line.strip())
        record = dist_info / "RECORD"
        if record.is_file():
            with open(record, newline="", encoding="utf-8", errors="replace") as handle:
                for row in csv.reader(handle):
                    if not row:
                        continue
                    by_file.setdefault(row[0].replace("\\", "/"), package)
                    top = _top_level_name(row[0])
                    if top:
                        top_names.add(top)
        for top in top_names:
            by_top.setdefault(top, package)
    return by_file, by_top


def determine_package(site_packages, quarantine_file, indexes=None):
    """Pakke og udgave for en karantænefil, eller None, hvis den ikke kan bestemmes."""
    by_file, by_top = indexes or build_indexes(site_packages)
    relative = Path(quarantine_file).relative_to(site_packages)
    original = relative.with_name(relative.name[: -len(".txt")]).as_posix()
    if original in by_file:
        return by_file[original]
    top = relative.parts[0]
    if len(relative.parts) == 1:
        top = original[: -len(".py")]
    return by_top.get(top)


def find_affected(site_packages):
    """Returnerer (pakker, ukendte): pakker -> deres karantænefiler, og filer uden pakke."""
    indexes = build_indexes(site_packages)
    affected = {}
    unknown = []
    for path in find_quarantine_files(site_packages):
        package = determine_package(site_packages, path, indexes)
        if package is None:
            unknown.append(path)
        else:
            affected.setdefault(package, []).append(path)
    return affected, unknown


def build_restore_command(venv_python, package):
    """Kommandoen, der geninstallerer netop denne pakke i samme udgave, uden andet."""
    return [
        str(venv_python), "-m", "pip", "install",
        "--force-reinstall", "--no-deps",
        f"{package.name}=={package.version}",
    ]


def run_command(command):
    """Selve kaldet til pakkehåndteringen (den eneste del, der bruger netværket)."""
    return subprocess.run(command, check=False).returncode


def check_import(venv_python):
    """Prøver at importere Django med miljøets Python. Returnerer (ok, fejltekst)."""
    result = subprocess.run(
        [str(venv_python), "-I", "-c", IMPORT_CHECK],
        capture_output=True, text=True, check=False,
    )
    if result.returncode == 0:
        return True, ""
    lines = [line for line in result.stderr.strip().splitlines() if line.strip()]
    return False, lines[-1] if lines else "ukendt fejl"


def _relative(path, site_packages):
    return Path(path).relative_to(site_packages).as_posix()


def main(argv=None, runner=run_command, importer=check_import, root=None, out=print):
    parser = argparse.ArgumentParser(
        description="Gendanner pakker i .venv, som sikkerhedstjenesten har sat i karantæne.",
    )
    parser.add_argument(
        "--tjek", action="store_true",
        help="Kun tjek og meld. Der ændres ingenting.",
    )
    args = parser.parse_args(argv)

    root = Path(root) if root else project_root()
    venv = root / ".venv"
    venv_python = find_venv_python(venv)
    site_packages = find_site_packages(venv)
    if venv_python is None or site_packages is None:
        out(f"Fandt ikke et virtuelt miljø (.venv) i {root}. Intet er ændret.")
        return EXIT_ERROR

    affected, unknown = find_affected(site_packages)

    if not affected and not unknown:
        out("Ingen filer er sat i karantæne i .venv.")
        ok, problem = importer(venv_python)
        if ok:
            out("Django kan importeres. Miljøet er i orden. Intet er ændret.")
            return EXIT_OK
        out(f"Django kan alligevel ikke importeres: {problem}")
        out("Det ligner ikke en karantæne. Miljøet skal undersøges på anden vis.")
        return EXIT_ERROR

    out("Disse filer er erstattet af en karantænetekst:")
    for package, files in affected.items():
        out(f"  Pakken {package.name} (udgave {package.version}):")
        for path in files:
            out(f"    {_relative(path, site_packages)}")
    for path in unknown:
        out(f"  Ukendt pakke: {_relative(path, site_packages)}")

    if unknown:
        out("Pakken bag nogle af filerne kan ikke bestemmes ud fra installationsoplysningerne, "
            "så de kan ikke gendannes af scriptet.")

    if args.tjek:
        out("Tjek-tilstand: intet er ændret. Kør scriptet uden --tjek for at gendanne pakkerne.")
        return EXIT_ERROR if unknown else EXIT_FOUND

    failed = False
    for package in affected:
        out(f"Gendanner {package.name} {package.version} ...")
        code = runner(build_restore_command(venv_python, package))
        if code != 0:
            out(f"Gendannelsen af {package.name} mislykkedes (pakkehåndteringen gav fejlkode {code}). "
                "Tjek netforbindelsen, og prøv igen.")
            failed = True
        else:
            out(f"{package.name} {package.version} er gendannet.")

    ok, problem = importer(venv_python)
    if ok:
        out("Django kan importeres.")
    else:
        out(f"Django kan stadig ikke importeres: {problem}")
        failed = True

    if failed or unknown:
        out("Miljøet er ikke i orden endnu. Se meldingerne ovenfor.")
        return EXIT_ERROR

    out("Miljøet er gendannet. Filen kan blive sat i karantæne igen. "
        "Sker det, så kør scriptet igen.")
    return EXIT_OK


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(errors="replace")
    except AttributeError:
        pass
    sys.exit(main())
