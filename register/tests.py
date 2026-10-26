from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from audit.models import AuditLog

from .models import Borger


class BorgerRegisterTests(TestCase):
    def setUp(self):
        self.client.force_login(get_user_model().objects.create_user("tester", password="x-test-adgangskode-1"))

    def opret(self, **kw):
        data = {"navn": "Person X", "cpr": "010203-0405", "tj_nr": "1", "afstand_km": "3.5", "transport": "selv", "zoner": "2", "sats": "20", "traek_procent": "40", "aktiv": "on"}
        data.update(kw)
        return self.client.post(reverse("borger_ny"), data)

    def test_opret_borger_normaliserer_cpr_og_logger(self):
        svar = self.opret(cpr="0102030405")
        self.assertRedirects(svar, reverse("borger_liste"))
        b = Borger.objects.get()
        self.assertEqual(b.cpr, "010203-0405")
        self.assertEqual(b.zoner, 2)
        self.assertTrue(AuditLog.objects.filter(handling="Oprettede medarbejder").exists())
        self.assertNotIn("0405", AuditLog.objects.get(handling="Oprettede medarbejder").detaljer)

    def test_ugyldigt_cpr_afvises(self):
        svar = self.opret(cpr="123")
        self.assertEqual(svar.status_code, 200)
        self.assertEqual(Borger.objects.count(), 0)

    def test_cpr_vises_aldrig_i_liste_eller_redigeringsformular(self):
        self.opret()
        b = Borger.objects.get()
        liste = self.client.get(reverse("borger_liste")).content.decode()
        form = self.client.get(reverse("borger_ret", args=[b.pk])).content.decode()
        for html in (liste, form):
            self.assertNotIn("010203-0405", html)
        self.assertIn("******-0405", form)

    def test_tomt_cpr_felt_beholder_eksisterende_cpr(self):
        self.opret()
        b = Borger.objects.get()
        self.client.post(
            reverse("borger_ret", args=[b.pk]),
            {"navn": "Nyt navn", "cpr": "", "tj_nr": "1", "afstand_km": "9", "transport": "taxa", "zoner": "", "sats": "20", "traek_procent": "40", "aktiv": "on"},
        )
        b.refresh_from_db()
        self.assertEqual((b.navn, b.cpr, b.afstand_km), ("Nyt navn", "010203-0405", Decimal("9.0")))

    def test_vis_cpr_kraever_post_og_logges(self):
        self.opret()
        b = Borger.objects.get()
        self.assertEqual(self.client.get(reverse("vis_cpr", args=[b.pk])).status_code, 405)
        svar = self.client.post(reverse("vis_cpr", args=[b.pk]), follow=True)
        self.assertContains(svar, "010203-0405")
        self.assertTrue(AuditLog.objects.filter(handling="Viste CPR", objekt_id=str(b.pk)).exists())

    def test_tj_nr_skal_vaere_unikt_men_kan_vaere_tomt(self):
        self.opret(navn="A", tj_nr="")
        self.opret(navn="B", tj_nr="")
        self.assertEqual(Borger.objects.count(), 2)
        svar = self.opret(navn="C", tj_nr="7")
        svar = self.opret(navn="D", tj_nr="7")
        self.assertEqual(svar.status_code, 200)
        self.assertEqual(Borger.objects.count(), 3)
