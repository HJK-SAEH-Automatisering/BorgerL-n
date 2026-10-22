import os
import runpy
import tempfile
from pathlib import Path
from unittest import mock

from django.test import SimpleTestCase

from config import settings

# Opdigtede nøgler; de findes ikke i projektets .env.example.
NOEGLE_A = "BORGERLON_TEST_A"
NOEGLE_B = "BORGERLON_TEST_B"


class LoadEnvTests(SimpleTestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)
        # Rydder de opdigtede nøgler efter testen, uanset hvad testen satte.
        patcher = mock.patch.dict(os.environ)
        patcher.start()
        self.addCleanup(patcher.stop)
        os.environ.pop(NOEGLE_A, None)
        os.environ.pop(NOEGLE_B, None)

    def skriv_env(self, indhold):
        sti = self.dir / ".env"
        sti.write_text(indhold, encoding="utf-8")
        return sti

    def test_noegler_fra_env_bruges(self):
        sti = self.skriv_env(f"{NOEGLE_A}=a-vaerdi\n# kommentar\n{NOEGLE_B}=\"b vaerdi\"\n")
        settings.load_env(sti)
        self.assertEqual(os.environ[NOEGLE_A], "a-vaerdi")
        self.assertEqual(os.environ[NOEGLE_B], "b vaerdi")

    def test_maskinens_vaerdi_vinder_over_env(self):
        os.environ[NOEGLE_A] = "fra-maskinen"
        sti = self.skriv_env(f"{NOEGLE_A}=fra-filen\n{NOEGLE_B}=fra-filen\n")
        settings.load_env(sti)
        self.assertEqual(os.environ[NOEGLE_A], "fra-maskinen")
        self.assertEqual(os.environ[NOEGLE_B], "fra-filen")

    def test_manglende_env_goer_ingenting(self):
        foer = dict(os.environ)
        with mock.patch("sys.stdout") as stdout, mock.patch("sys.stderr") as stderr:
            settings.load_env(self.dir / ".env")
        self.assertEqual(dict(os.environ), foer)
        stdout.write.assert_not_called()
        stderr.write.assert_not_called()

    def test_indstillingerne_soeger_env_i_projektroden_ikke_i_arbejdsmappen(self):
        self.skriv_env(f"{NOEGLE_A}=fra-arbejdsmappen\n")
        foer = Path.cwd()
        os.chdir(self.dir)
        self.addCleanup(os.chdir, foer)
        runpy.run_path(settings.__file__)
        self.assertNotIn(NOEGLE_A, os.environ)
