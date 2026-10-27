"""Tests af scripts/reparer_miljo.py. Ingen kald til pakkeregistret.

Kør uden Django:  .venv\\Scripts\\python.exe -m unittest scripts.test_reparer_miljo
De indgår også i:  .venv\\Scripts\\python.exe manage.py test
"""

import tempfile
import unittest
from pathlib import Path

from scripts import reparer_miljo as rm

QUARANTINE_TEXT = "This file is quarantined all because it triggered Web Reputation.\r\n"


class MiljoTestCase(unittest.TestCase):
    """Bygger et opdigtet projekt med .venv i en midlertidig mappe."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.venv = self.root / ".venv"
        (self.venv / "Scripts").mkdir(parents=True)
        self.python = self.venv / "Scripts" / "python.exe"
        self.python.write_bytes(b"")
        self.site = self.venv / "Lib" / "site-packages"
        self.site.mkdir(parents=True)

    def add_package(self, name, version, dirname, files, top_level=True):
        """Opretter en pakkemappe med filer og en dist-info."""
        dist_info = self.site / f"{dirname}-{version}.dist-info"
        dist_info.mkdir()
        (dist_info / "METADATA").write_text(
            f"Metadata-Version: 2.1\nName: {name}\nVersion: {version}\n", encoding="utf-8"
        )
        record = []
        for relative in files:
            path = self.site / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("x = 1\n", encoding="utf-8")
            record.append(f"{relative},sha256=abc,6")
        (dist_info / "RECORD").write_text("\n".join(record) + "\n", encoding="utf-8")
        if top_level:
            (dist_info / "top_level.txt").write_text(files[0].split("/")[0].replace(".py", "") + "\n")

    def quarantine(self, relative, content=QUARANTINE_TEXT, encoding="utf-8"):
        """Erstatter relative (en .py-fil) med relative + '.txt' med den givne tekst."""
        original = self.site / relative
        if original.exists():
            original.unlink()
        target = self.site / (relative + ".txt")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content.encode(encoding))
        return target

    def snapshot(self):
        return sorted(
            (str(p.relative_to(self.root)), p.read_bytes() if p.is_file() else None)
            for p in self.root.rglob("*")
        )

    def run_main(self, argv=(), import_ok=True):
        commands = []

        def runner(command):
            commands.append(command)
            return 0

        messages = []
        code = rm.main(
            list(argv),
            runner=runner,
            importer=lambda python: (import_ok, "" if import_ok else "No module named x"),
            root=self.root,
            out=messages.append,
        )
        return code, commands, "\n".join(messages)


class FindQuarantineFilesTest(MiljoTestCase):
    def setUp(self):
        super().setUp()
        self.add_package("Django", "6.1.2", "django", ["django/__init__.py", "django/utils/cache.py"])

    def test_healthy_environment_has_no_findings(self):
        self.assertEqual(rm.find_quarantine_files(self.site), [])

    def test_finds_quarantine_file(self):
        target = self.quarantine("django/utils/cache.py")
        self.assertEqual(rm.find_quarantine_files(self.site), [target])

    def test_finds_quarantine_file_with_bom(self):
        target = self.quarantine("django/utils/cache.py", "\ufeff" + QUARANTINE_TEXT)
        self.assertEqual(rm.find_quarantine_files(self.site), [target])

    def test_finds_utf16_quarantine_file(self):
        target = self.quarantine("django/utils/cache.py", QUARANTINE_TEXT, "utf-16")
        self.assertEqual(rm.find_quarantine_files(self.site), [target])

    def test_ignores_py_txt_that_is_not_quarantine(self):
        (self.site / "django" / "notes.py.txt").write_text("Almindelig tekst.\n", encoding="utf-8")
        self.assertEqual(rm.find_quarantine_files(self.site), [])

    def test_ignores_other_files_with_the_message(self):
        (self.site / "django" / "readme.txt").write_text(QUARANTINE_TEXT, encoding="utf-8")
        self.assertEqual(rm.find_quarantine_files(self.site), [])

    def test_ignores_old_quarantine_file_when_original_is_back(self):
        (self.site / "django" / "utils" / "cache.py.txt").write_text(QUARANTINE_TEXT, encoding="utf-8")
        self.assertEqual(rm.find_quarantine_files(self.site), [])


class DeterminePackageTest(MiljoTestCase):
    def test_name_and_version_differ_from_directory_name(self):
        self.add_package("Django", "6.1.2", "django", ["django/__init__.py", "django/utils/cache.py"])
        target = self.quarantine("django/utils/cache.py")
        package = rm.determine_package(self.site, target)
        self.assertEqual((package.name, package.version), ("Django", "6.1.2"))

    def test_uses_top_level_when_record_is_missing(self):
        self.add_package("PyYAML", "6.0", "PyYAML", ["yaml/__init__.py"])
        (self.site / "PyYAML-6.0.dist-info" / "RECORD").unlink()
        target = self.quarantine("yaml/loader.py")
        package = rm.determine_package(self.site, target)
        self.assertEqual((package.name, package.version), ("PyYAML", "6.0"))

    def test_uses_record_when_top_level_is_missing(self):
        self.add_package("Django", "6.1.2", "django", ["django/__init__.py", "django/utils/cache.py"],
                         top_level=False)
        target = self.quarantine("django/utils/cache.py")
        package = rm.determine_package(self.site, target)
        self.assertEqual(package.version, "6.1.2")

    def test_single_module_package(self):
        self.add_package("six", "1.17.0", "six", ["six.py"])
        target = self.quarantine("six.py")
        package = rm.determine_package(self.site, target)
        self.assertEqual((package.name, package.version), ("six", "1.17.0"))

    def test_unknown_package_gives_none(self):
        target = self.quarantine("ukendt/modul.py")
        self.assertIsNone(rm.determine_package(self.site, target))

    def test_unsafe_name_in_metadata_is_not_used(self):
        self.add_package("--index-url=x", "1.0", "ond", ["ond/__init__.py"])
        target = self.quarantine("ond/a.py")
        self.assertIsNone(rm.determine_package(self.site, target))


class BuildRestoreCommandTest(unittest.TestCase):
    def test_command_is_for_exactly_that_package_and_version(self):
        command = rm.build_restore_command(Path("venv/python.exe"), rm.Package("Django", "6.1.2"))
        self.assertEqual(command, [
            str(Path("venv/python.exe")), "-m", "pip", "install",
            "--force-reinstall", "--no-deps", "Django==6.1.2",
        ])


class MainTest(MiljoTestCase):
    def setUp(self):
        super().setUp()
        self.add_package("Django", "6.1.2", "django", ["django/__init__.py", "django/utils/cache.py"])
        self.add_package("sqlparse", "0.6.0", "sqlparse", ["sqlparse/__init__.py"])

    def test_healthy_environment_is_left_unchanged(self):
        before = self.snapshot()
        code, commands, text = self.run_main()
        self.assertEqual(code, 0)
        self.assertEqual(commands, [])
        self.assertIn("i orden", text)
        self.assertEqual(self.snapshot(), before)

    def test_healthy_but_django_not_importable_is_an_error(self):
        code, commands, text = self.run_main(import_ok=False)
        self.assertEqual(code, rm.EXIT_ERROR)
        self.assertEqual(commands, [])
        self.assertIn("ikke importeres", text)

    def test_check_mode_reports_and_changes_nothing(self):
        self.quarantine("django/utils/cache.py")
        before = self.snapshot()
        code, commands, text = self.run_main(["--tjek"])
        self.assertEqual(code, rm.EXIT_FOUND)
        self.assertEqual(commands, [])
        self.assertIn("Django", text)
        self.assertIn("6.1.2", text)
        self.assertIn("django/utils/cache.py.txt", text)
        self.assertEqual(self.snapshot(), before)

    def test_restore_is_called_for_exactly_the_affected_package(self):
        self.quarantine("django/utils/cache.py")
        code, commands, text = self.run_main()
        self.assertEqual(code, 0)
        self.assertEqual(commands, [rm.build_restore_command(self.python, rm.Package("Django", "6.1.2"))])
        self.assertIn("Django kan importeres", text)
        self.assertIn("kør scriptet igen", text)

    def test_each_affected_package_is_restored_once(self):
        self.quarantine("django/utils/cache.py")
        self.quarantine("django/__init__.py")
        self.quarantine("sqlparse/__init__.py")
        code, commands, _ = self.run_main()
        self.assertEqual(code, 0)
        self.assertEqual(sorted(c[-1] for c in commands), ["Django==6.1.2", "sqlparse==0.6.0"])

    def test_failed_restore_gives_error_code(self):
        self.quarantine("django/utils/cache.py")
        messages = []
        code = rm.main([], runner=lambda command: 1, importer=lambda p: (False, "No module named x"),
                       root=self.root, out=messages.append)
        self.assertEqual(code, rm.EXIT_ERROR)
        self.assertIn("mislykkedes", "\n".join(messages))

    def test_import_failure_after_restore_gives_error_code(self):
        self.quarantine("django/utils/cache.py")
        code, commands, text = self.run_main(import_ok=False)
        self.assertEqual(code, rm.EXIT_ERROR)
        self.assertEqual(len(commands), 1)
        self.assertIn("stadig ikke importeres", text)

    def test_unknown_package_is_not_restored_and_gives_error_code(self):
        self.quarantine("ukendt/modul.py")
        code, commands, text = self.run_main()
        self.assertEqual(code, rm.EXIT_ERROR)
        self.assertEqual(commands, [])
        self.assertIn("ukendt/modul.py.txt", text)

    def test_missing_venv_is_reported(self):
        messages = []
        code = rm.main([], root=self.root / "findes-ikke", out=messages.append)
        self.assertEqual(code, rm.EXIT_ERROR)
        self.assertIn(".venv", "\n".join(messages))


if __name__ == "__main__":
    unittest.main()
