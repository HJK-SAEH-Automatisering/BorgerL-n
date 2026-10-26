import os
import shutil
import tempfile
from decimal import Decimal
from pathlib import Path

from django.contrib.auth import get_user_model
from django.template import Context, Template
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from register.models import Borger

from .models import Koersel
from .tests import xlsx


def vis(sti):
    return Template("{% load asset_tags %}{% static_v '" + sti + "' %}").render(Context())


class StaticVersionTests(SimpleTestCase):
    def setUp(self):
        self.mappe = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.mappe, ignore_errors=True)
        self.fil = self.mappe / "test.css"
        self.fil.write_text("body {}")
        os.utime(self.fil, ns=(1_000_000_000_000_000_000, 1_000_000_000_000_000_000))
        override = override_settings(STATICFILES_DIRS=[self.mappe])
        override.enable()
        self.addCleanup(override.disable)

    def test_adressen_har_en_version(self):
        self.assertRegex(vis("test.css"), r"^/static/test\.css\?v=\d+$")

    def test_versionen_er_den_samme_naar_filen_er_uaendret(self):
        self.assertEqual(vis("test.css"), vis("test.css"))

    def test_versionen_skifter_naar_filens_aendringstidspunkt_skifter(self):
        foer = vis("test.css")
        os.utime(self.fil, ns=(2_000_000_000_000_000_000, 2_000_000_000_000_000_000))
        efter = vis("test.css")
        self.assertNotEqual(foer, efter)
        self.assertTrue(efter.startswith("/static/test.css?v="))

    def test_manglende_fil_giver_adresse_uden_version(self):
        self.assertEqual(vis("findes-ikke.css"), "/static/findes-ikke.css")


class SiderneBrugerVersionTests(TestCase):
    def setUp(self):
        self.client.force_login(get_user_model().objects.create_user("tester", password="x-test-adgangskode-1"))

    def test_stilarket_har_version_paa_en_side_med_login(self):
        html = self.client.get(reverse("dashboard")).content.decode()
        self.assertRegex(html, r'href="/static/css/app\.css\?v=\d+"')

    def test_stilarket_har_version_paa_loginsiden(self):
        self.client.logout()
        html = self.client.get(reverse("login")).content.decode()
        self.assertRegex(html, r'href="/static/css/app\.css\?v=\d+"')

    def test_undtagelser_har_version_paa_baade_stilark_og_skaermkode(self):
        Borger.objects.create(navn="Person 1", tj_nr="9001", cpr="000000-0001", sats=Decimal("20"), afstand_km=Decimal("4.7"), transport="selv", zoner=2)
        self.client.post(reverse("dashboard"), {"maaned": "2026-10"})
        k = Koersel.objects.get()
        self.client.post(reverse("upload", args=[k.pk]), {"fil": xlsx([("Person 1", "44:12")])})
        html = self.client.get(reverse("undtagelser", args=[k.pk])).content.decode()
        self.assertRegex(html, r'href="/static/css/app\.css\?v=\d+"')
        self.assertRegex(html, r'src="/static/js/undtagelser\.js\?v=\d+"')
