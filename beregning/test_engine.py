from decimal import Decimal as D
from unittest import TestCase

from beregning.engine import Input, Parametre, Zonepris, beregn

PAR = Parametre(max_egenbetaling_procent=D("30"), afstandskrav_km=D("10"), grundtakst=D("217.50"))
ZONER = {
    2: Zonepris(kontant_barn=D("12"), pendler_barn=D("217.5")),
    3: Zonepris(kontant_barn=D("17"), pendler_barn=D("292.5")),
}


def inp(**kw):
    basis = dict(navn="Person 1", minutter=44 * 60 + 12, sats=D("20"), traek_procent=D("40"), transport="selv", zoner=2, afstand_km=D("3.2"))
    basis.update(kw)
    return Input(**basis)


class LoenTests(TestCase):
    def test_loen_foer_og_efter_skat_matcher_arket(self):
        r = beregn(inp(transport="ingen"), PAR, ZONER)
        self.assertEqual(r.loen_foer, D("884.00"))
        self.assertEqual(r.skattetraek, D("353"))
        self.assertEqual(r.loen_efter, D("531.00"))

    def test_skattetraek_rundes_ned_til_hele_kroner(self):
        r = beregn(inp(minutter=60, sats=D("12.50"), transport="ingen"), PAR, ZONER)
        self.assertEqual(r.loen_foer, D("12.50"))
        self.assertEqual(r.skattetraek, D("5"))
        self.assertEqual(r.loen_efter, D("7.50"))


class TransportTests(TestCase):
    def test_egenbetaling_er_30_procent_naar_det_er_under_grundtakst(self):
        r = beregn(inp(), PAR, ZONER)
        self.assertEqual(r.egenbetaling, D("159.30"))

    def test_egenbetaling_loftes_af_grundtakst(self):
        r = beregn(inp(minutter=100 * 60, sats=D("30")), PAR, ZONER)
        self.assertEqual(r.egenbetaling, D("217.50"))

    def test_kører_selv_to_zoner(self):
        r = beregn(inp(zoner=2), PAR, ZONER)
        self.assertEqual(r.udbetaling_991, D("58.20"))
        self.assertEqual(r.traek_991, D("0"))

    def test_kører_selv_tre_zoner(self):
        r = beregn(inp(zoner=3), PAR, ZONER)
        self.assertEqual(r.udbetaling_991, D("133.20"))

    def test_individuel_udgift_under_egenbetaling_giver_nul(self):
        r = beregn(inp(zoner=3, individuel=True, dage=4), PAR, ZONER)
        self.assertEqual(r.udbetaling_991, D("0.00"))

    def test_individuel_beregning_med_hoej_nok_udgift(self):
        r = beregn(inp(zoner=3, individuel=True, dage=20, minutter=100 * 60, sats=D("30")), PAR, ZONER)
        self.assertEqual(r.udbetaling_991, D("2") * D("17") * D("20") - D("217.50"))

    def test_taxa_traekker_egenbetaling_og_udbetaler_intet(self):
        r = beregn(inp(transport="taxa", zoner=None), PAR, ZONER)
        self.assertEqual(r.traek_991, D("159.30"))
        self.assertEqual(r.udbetaling_991, D("0"))

    def test_ingen_udgift_giver_ingen_posteringer(self):
        r = beregn(inp(transport="ingen", zoner=None), PAR, ZONER)
        self.assertEqual((r.traek_991, r.udbetaling_991), (D("0"), D("0")))

    def test_ingen_timer_ingen_udbetaling(self):
        r = beregn(inp(minutter=0), PAR, ZONER)
        self.assertTrue(r.ok)
        self.assertEqual(r.udbetaling_991, D("0"))
        self.assertIn("Ingen timer registreret i perioden.", r.advarsler)


class ValideringTests(TestCase):
    def test_manglende_transport(self):
        r = beregn(inp(transport=""), PAR, ZONER)
        self.assertEqual(r.fejl, ["Transport mangler."])
        self.assertEqual(r.grundlag, [])

    def test_manglende_zone_er_fejl_ikke_et_tal(self):
        r = beregn(inp(zoner=None), PAR, ZONER)
        self.assertEqual(r.fejl, ["Zone mangler."])

    def test_ukendt_zone(self):
        r = beregn(inp(zoner=9), PAR, ZONER)
        self.assertEqual(r.fejl, ["Zone 9 findes ikke i zonetabellen."])

    def test_individuel_kraever_dage(self):
        r = beregn(inp(individuel=True, dage=None), PAR, ZONER)
        self.assertEqual(r.fejl, ["Fremmødedage mangler (1-31)."])

    def test_individuel_kraever_kører_selv(self):
        r = beregn(inp(transport="taxa", individuel=True, dage=3), PAR, ZONER)
        self.assertTrue(r.fejl)

    def test_manglende_sats(self):
        r = beregn(inp(sats=None), PAR, ZONER)
        self.assertIn("Sats pr. time mangler på medarbejderen.", r.fejl)


class AdvarselTests(TestCase):
    def test_dobbeltansaettelse(self):
        r = beregn(inp(dobbelt=True), PAR, ZONER)
        self.assertTrue(any("dobbeltansættelse" in a for a in r.advarsler))

    def test_lang_afstand_med_to_zoner(self):
        r = beregn(inp(afstand_km=D("13.2"), zoner=2), PAR, ZONER)
        self.assertTrue(any("over 10 km" in a for a in r.advarsler))

    def test_grundlag_har_nummererede_trin(self):
        r = beregn(inp(), PAR, ZONER)
        self.assertEqual([t["nr"] for t in r.grundlag], list(range(1, len(r.grundlag) + 1)))
        self.assertTrue(all(t["formel"] and t["resultat"] for t in r.grundlag))
