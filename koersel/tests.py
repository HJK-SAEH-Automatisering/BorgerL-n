import hashlib
import shutil
import tempfile
from datetime import date, time, timedelta
from decimal import Decimal
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from openpyxl import Workbook

from audit.models import AuditLog
from beregning.pdf import lav_rapport
from register.models import Borger

from .importer import ImportFejl, laes_timefil
from .models import Koersel, Linje


def xlsx(raekker, header=("Navn", "Total timer (timer:minutter)"), navn="timer.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws["C4"], ws["D4"] = header
    for i, (n, t) in enumerate(raekker, start=5):
        ws.cell(row=i, column=3, value=n)
        ws.cell(row=i, column=4, value=t)
    buf = BytesIO()
    wb.save(buf)
    return SimpleUploadedFile(navn, buf.getvalue())


class ImporterTests(TestCase):
    def test_laeser_tekst_tider(self):
        r = laes_timefil(xlsx([("Person 1", "79:25"), ("Person 2", "8:49")]))
        self.assertEqual([(x.navn, x.minutter) for x in r], [("Person 1", 79 * 60 + 25), ("Person 2", 8 * 60 + 49)])

    def test_laeser_excel_tidsceller(self):
        r = laes_timefil(xlsx([("A", time(8, 30)), ("B", timedelta(hours=100, minutes=58)), ("C", 0.5)]))
        self.assertEqual([x.minutter for x in r], [510, 6058, 720])

    def test_afviser_forkert_filtype(self):
        with self.assertRaisesMessage(ImportFejl, ".xlsx"):
            laes_timefil(SimpleUploadedFile("timer.csv", b"Navn;Timer"))

    def test_afviser_ikke_excel_indhold(self):
        with self.assertRaises(ImportFejl):
            laes_timefil(SimpleUploadedFile("timer.xlsx", b"ikke en excel-fil"))

    def test_afviser_beskadiget_excel_fil_uden_at_crashe(self):
        god = bytearray(xlsx([("A", "1:00")]).read())
        for i in range(120, 260):
            god[i] = 0
        with self.assertRaisesMessage(ImportFejl, "kan ikke læses"):
            laes_timefil(SimpleUploadedFile("timer.xlsx", bytes(god)))

    def test_mangler_kolonner(self):
        with self.assertRaisesMessage(ImportFejl, "Kunne ikke finde kolonnerne"):
            laes_timefil(xlsx([("A", "1:00")], header=("Person", "Antal")))

    def test_ugyldigt_tidsformat_peger_paa_raekken(self):
        with self.assertRaisesMessage(ImportFejl, "Række 6 (B)"):
            laes_timefil(xlsx([("A", "1:00"), ("B", "meget")]))


TEST_MEDIA = tempfile.mkdtemp(prefix="borgerlon-test-")


@override_settings(MEDIA_ROOT=TEST_MEDIA)
class FlowTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA, ignore_errors=True)

    def setUp(self):
        self.bruger = get_user_model().objects.create_user("tester", password="x-test-adgangskode-1")
        self.client.force_login(self.bruger)
        self.p1 = Borger.objects.create(navn="Person 1", tj_nr="9001", cpr="000000-0001", sats=Decimal("20"), afstand_km=Decimal("4.7"), transport="selv", zoner=2)
        self.p2 = Borger.objects.create(navn="Person 2", tj_nr="9002", cpr="000000-0002", sats=Decimal("20"), afstand_km=Decimal("2"), transport="taxa")
        self.p3 = Borger.objects.create(navn="Person 3", tj_nr="9003", cpr="000000-0003", sats=Decimal("20"), afstand_km=Decimal("13.2"), transport="selv")

    def opret_og_upload(self, raekker):
        self.client.post(reverse("dashboard"), {"maaned": "2026-10"})
        k = Koersel.objects.get()
        svar = self.client.post(reverse("upload", args=[k.pk]), {"fil": xlsx(raekker, navn="punchly.xlsx")})
        self.assertRedirects(svar, reverse("gennemse", args=[k.pk]))
        return k

    def undtagelser(self, k, **valg):
        data = {"handling": valg.pop("handling", "beregn")}
        for l in k.linjer.all():
            data.update({f"t_{l.pk}": l.transport, f"z_{l.pk}": l.zoner or ""})
            if l.individuel:
                data[f"i_{l.pk}"] = "on"
                data[f"d_{l.pk}"] = l.dage or ""
        data.update(valg)
        return self.client.post(reverse("undtagelser", args=[k.pk]), data)

    def test_upload_matcher_paa_navn(self):
        k = self.opret_og_upload([("Person 1", "44:12"), ("  person 2 ", "10:00"), ("Ukendt", "5:00")])
        status = {l.fil_navn.strip(): l.match_status for l in k.linjer.all()}
        self.assertEqual(status, {"Person 1": "matchet", "person 2": "matchet", "Ukendt": "ingen"})

    def test_upload_gemmer_hvem_og_hvornaar_og_viser_det(self):
        k = self.opret_og_upload([("Person 1", "44:12")])
        k.refresh_from_db()
        self.assertEqual(k.uploadet_af, self.bruger)
        self.assertIsNotNone(k.uploadet)
        svar = self.client.get(reverse("upload", args=[k.pk]))
        self.assertContains(svar, "Sidst uploadet: punchly.xlsx, af tester, ")
        self.assertContains(svar, timezone.localtime(k.uploadet).strftime("%d.%m.%Y kl. %H:%M"))

    def test_ny_upload_erstatter_fil_bruger_og_tidspunkt(self):
        k = self.opret_og_upload([("Person 1", "44:12")])
        foer = timezone.now() - timedelta(days=3)
        Koersel.objects.filter(pk=k.pk).update(uploadet=foer)
        anden = get_user_model().objects.create_user("anden", password="x-test-adgangskode-2")
        self.client.force_login(anden)
        self.client.post(reverse("upload", args=[k.pk]), {"fil": xlsx([("Person 2", "1:00")], navn="ny.xlsx")})
        k.refresh_from_db()
        self.assertEqual((k.filnavn, k.uploadet_af), ("ny.xlsx", anden))
        self.assertGreater(k.uploadet, foer)
        svar = self.client.get(reverse("upload", args=[k.pk]))
        self.assertContains(svar, "Sidst uploadet: ny.xlsx, af anden, ")
        self.assertNotContains(svar, "punchly.xlsx")

    def test_afvist_upload_aendrer_ikke_sidst_uploadet(self):
        k = self.opret_og_upload([("Person 1", "44:12")])
        foer = Koersel.objects.get(pk=k.pk)
        self.client.post(reverse("upload", args=[k.pk]), {"fil": SimpleUploadedFile("daarlig.xlsx", b"ikke en excel-fil")})
        efter = Koersel.objects.get(pk=k.pk)
        self.assertEqual((efter.filnavn, efter.uploadet_af, efter.uploadet), (foer.filnavn, foer.uploadet_af, foer.uploadet))

    def test_koersel_uploadet_foer_felterne_viser_kun_filnavn(self):
        k = Koersel.objects.create(maaned=date(2026, 9, 1), filnavn="gammel.xlsx")
        svar = self.client.get(reverse("upload", args=[k.pk]))
        self.assertContains(svar, "Sidst uploadet: gammel.xlsx<")
        self.assertNotContains(svar, ", af ")
        self.assertNotContains(svar, " kl. ")

    def test_slettet_bruger_viser_filnavn_og_tidspunkt_uden_navn(self):
        k = self.opret_og_upload([("Person 1", "44:12")])
        self.bruger.delete()
        self.client.force_login(get_user_model().objects.create_user("ny", password="x-test-adgangskode-3"))
        k.refresh_from_db()
        self.assertIsNone(k.uploadet_af)
        svar = self.client.get(reverse("upload", args=[k.pk]))
        self.assertContains(svar, "Sidst uploadet: punchly.xlsx, ")
        self.assertNotContains(svar, ", af ")
        self.assertContains(svar, " kl. ")

    def test_uden_upload_staar_der_ingen_fil_valgt(self):
        k = Koersel.objects.create(maaned=date(2026, 9, 1))
        self.assertContains(self.client.get(reverse("upload", args=[k.pk])), "Ingen fil valgt")

    def test_flertydigt_navn_afklares_aldrig_automatisk(self):
        Borger.objects.create(navn="Person 1", tj_nr="9101")
        k = self.opret_og_upload([("Person 1", "1:00")])
        l = k.linjer.get()
        self.assertEqual(l.match_status, Linje.Match.FLERTYDIG)
        self.assertIsNone(l.borger)

    def test_uafklarede_raekker_blokerer_videre_flow(self):
        k = self.opret_og_upload([("Ukendt", "5:00")])
        svar = self.client.get(reverse("undtagelser", args=[k.pk]))
        self.assertRedirects(svar, reverse("gennemse", args=[k.pk]))
        svar = self.client.post(reverse("gennemse", args=[k.pk]), {"handling": "fortsaet"})
        self.assertRedirects(svar, reverse("gennemse", args=[k.pk]))

    def test_afklar_raekke_og_gem_rettelser_i_registret(self):
        k = self.opret_og_upload([("Ukendt", "5:00")])
        l = k.linjer.get()
        self.client.post(reverse("gennemse", args=[k.pk]), {"handling": "afklar", "linje": l.pk, "borger": self.p2.pk})
        l.refresh_from_db()
        self.assertEqual(l.borger, self.p2)
        self.client.post(reverse("gennemse", args=[k.pk]), {"handling": "gem", f"afstand_{l.pk}": "7,5", f"transport_{l.pk}": "ingen"})
        self.p2.refresh_from_db()
        self.assertEqual((self.p2.afstand_km, self.p2.transport), (Decimal("7.5"), "ingen"))
        self.assertTrue(AuditLog.objects.filter(handling="Ændrede borger fra gennemsyn").exists())

    def test_beregn_afvises_naar_zone_mangler(self):
        k = self.opret_og_upload([("Person 3", "44:12")])
        svar = self.undtagelser(k)
        self.assertEqual(svar.status_code, 200)
        self.assertContains(svar, "Mangler zone")
        self.assertEqual(k.beregninger.count(), 0)

    def test_hele_flowet_beregn_pdf_godkend_eksport(self):
        k = self.opret_og_upload([("Person 1", "44:12"), ("Person 2", "10:00")])
        svar = self.undtagelser(k)
        self.assertRedirects(svar, reverse("godkend", args=[k.pk]))
        b = k.beregninger.get()

        pdf = b.pdf.read()
        self.assertTrue(pdf.startswith(b"%PDF"))
        self.assertEqual(hashlib.sha256(pdf).hexdigest(), b.pdf_sha256)
        self.assertEqual(hashlib.sha256(lav_rapport(b.data)).hexdigest(), b.pdf_sha256)
        self.assertNotIn("000000-0001", b.snapshot)

        r1 = b.resultater.get(navn="Person 1")
        self.assertEqual(r1.loen_foer, Decimal("884.00"))
        self.assertEqual(r1.loen_efter, Decimal("531.00"))
        self.assertEqual(r1.udbetaling_991, Decimal("58.20"))

        spaerret = self.client.get(reverse("eksport", args=[k.pk]))
        self.assertRedirects(spaerret, reverse("godkend", args=[k.pk]))

        self.client.post(reverse("godkend", args=[k.pk]), {"handling": "godkend", "resultat": r1.pk})
        self.assertEqual(self.client.get(reverse("eksport", args=[k.pk])).status_code, 302)

        self.client.post(reverse("godkend", args=[k.pk]), {"handling": "godkend_alle"})
        k.refresh_from_db()
        self.assertEqual(k.status, Koersel.Status.GODKENDT)
        svar = self.client.get(reverse("eksport", args=[k.pk]))
        self.assertEqual(svar.status_code, 200)
        self.assertIn("Person 1", svar.content.decode("utf-8-sig"))

        self.assertEqual(self.client.get(reverse("rapport", args=[b.pk])).status_code, 200)

    def test_ny_beregning_ophaever_tidligere_godkendelser(self):
        k = self.opret_og_upload([("Person 1", "44:12")])
        self.undtagelser(k)
        self.client.post(reverse("godkend", args=[k.pk]), {"handling": "godkend_alle"})
        self.client.post(reverse("godkend", args=[k.pk]), {"handling": "genaabn"})
        self.undtagelser(k)
        self.assertEqual(k.beregninger.count(), 2)
        ny = k.aktiv_beregning
        self.assertEqual(ny.nummer, 2)
        self.assertFalse(ny.alle_godkendt)
        k.refresh_from_db()
        self.assertEqual(k.status, Koersel.Status.BEREGNET)
        self.assertEqual(self.client.get(reverse("eksport", args=[k.pk])).status_code, 302)
        self.assertTrue(k.beregninger.get(nummer=1).pdf)

    def test_kraever_login(self):
        self.client.logout()
        for navn, args in (("dashboard", []), ("borger_liste", []), ("godkend", [1]), ("rapport", [1])):
            svar = self.client.get(reverse(navn, args=args))
            self.assertEqual(svar.status_code, 302, navn)
            self.assertIn("/konto/login/", svar["Location"])
