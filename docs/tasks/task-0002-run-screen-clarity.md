---
nummer: task-0002
titel: Tydeligere kørselsskærme: sidst uploadet og første manglende række
status: afsluttet
kilde: mockup-0002, mockup-0004
oprettet: 2026-10-22
---

# task-0002 — Tydeligere kørselsskærme: sidst uploadet og første manglende række

## Hvad og hvorfor
Denne opgave erstatter task-0001, som blev droppet; definitionen er den samme. Bygges forfra fra default-branch.

Slutbrugerne gennemgik skitser af de fire trin i månedens kørsel. To små ændringer blev tilbage; resten blev afvist (se beslutningsloggen).

1. Upload-skærmen viser kun filnavnet på sidst uploadede fil. Uploades en ny fil, erstattes rækkerne og alle rettelser i de senere trin. Brugeren skal kunne se hvem der uploadede og hvornår, før det sker.
2. På Undtagelser melder "Beregn" kun hvor mange borgere der mangler oplysninger. Brugeren skal selv finde rækkerne. "Beregn" skal i stedet føre brugeren til den første række der mangler noget.

De to er samlet i én opgave, fordi hver for sig er for lille til at bære en tråd, og begge ligger i kørselsskærmene.

## Færdig når
Upload:

- [ ] Efter en upload viser upload-skærmen "Sidst uploadet" med filnavn, brugerens navn, dato og klokkeslæt.
- [ ] Uploades en ny fil til samme måned, viser skærmen den nye fils navn, den nye bruger og det nye tidspunkt.
- [ ] En kørsel der blev uploadet, før ændringen kom, viser kun filnavnet og kan stadig åbnes og uploades igen uden fejl.
- [ ] Er den bruger der uploadede ikke længere i systemet, viser skærmen filnavn og tidspunkt uden navn og uden fejl.
- [ ] Er der ikke uploadet en fil, står der som i dag "Ingen fil valgt".

Undtagelser:

- [ ] Trykker brugeren "Beregn", mens mindst én borger mangler oplysninger, rulles siden til den første række der mangler noget, og rækken markeres tydeligt, så den kan ses på et øjeblik.
- [ ] Rulningen sker også når beregningen afvises af serveren, og siden indlæses igen med fejl.
- [ ] Meddelelsen om hvor mange der mangler, står stadig som i dag.
- [ ] Mangler ingen noget, beregnes kørslen som i dag, uden rulning.
- [ ] Alle regler for hvornår en række er klar, er uændrede.

Fælles:

- [ ] Der er ikke bygget filter, søgning, nye skærme eller nye knapper.
- [ ] Testsuiten er grøn, og de nye regler for upload har tests.

## Sådan bygger vi det
- **Upload.** Kørslen får to nye valgfrie felter: hvem der sidst uploadede, og hvornår. De sættes samme sted som filnavnet sættes i dag, når rækkerne oprettes. Kræver en ny migrering. Tomme felter for eksisterende kørsler.
- **Hvorfor felter og ikke auditloggen.** Auditloggen er fri tekst pr. handling; at slå op i den på handlingsteksten er skrøbeligt. Felterne på kørslen er dét skærmen viser, og de følger kørslen.
- **Visning.** Upload-skabelonen viser "Sidst uploadet: filnavn, af navn, dato og klokkeslæt" i dansk format. Dashboard og Gennemse transport viser stadig kun filnavnet.
- **Undtagelser.** Rulning og markering bygges i den eksisterende skærmkode. Rækken der mangler noget, har allerede en statusmarkering med klasse; den første række med en ikke-klar status findes ud fra den. Tilføj en markering på rækken, så den skiller sig ud, og fjern den igen, når rækken bliver klar eller brugeren retter noget.
- **Efter serverafvisning.** Når siden tegnes igen med fejl, kører den samme rulning ved indlæsning.
- Skærmkoden er lidt vanilla JS som i dag. Ingen build, ingen nye pakker.

## Hvad vi ikke rører
- Beregningsmotoren, snapshot og PDF-rapport.
- Importen: hvad der læses, og hvilke fejl der gives.
- Godkendelse, eksport, genåbn.
- Reglerne for status på Undtagelser: hvornår en række er klar, mangler transport, zone, dage eller sats.
- Auditlog: hvad der logges ved upload og gem.
- Dashboard og Gennemse transport.

## Afhænger af
intet. Men: sendes først af sted, når Django i `.venv` kan starte, så testene kan køres.

## Beslutninger
- BESLUTTET: Felter på kørslen frem for opslag i auditloggen — auditloggen er fri tekst og ikke stedet at hente visningsdata fra. Afvist: opslag på handlingsteksten "Uploadede timefil".
- BESLUTTET: Én opgave for de to ændringer — hver for sig er for lille til at bære en tråd, og begge ligger i kørselsskærmene. Afvist: to opgaver.
- BESLUTTET: Ingen filter "vis kun dem der mangler" på Undtagelser — rulning til første række løser det samme uden et nyt kontrolelement. Se beslutningsloggen.
- BESLUTTET: Dashboard og Gennemse transport uændrede — kun upload-skærmen har brug for at vide hvad der overskrives.
- BESLUTTET: Upload-skærmen viser brugernavnet, som resten af appen gør — det er det der står ved godkendelser. Afvist: fuldt navn, som kræver et nyt felt på brugeren.
- BESLUTTET: Afvises beregningen kun med generelle fejl, er der ingen række at rulle til, og meddelelsen øverst på siden er nok — ingen særlig behandling.

## Åbne punkter
intet


## Indvendinger
<Udfyldes af andre roller.>

---

## Developers noter

<Alt over denne overskrift ejes af architect. Alt herunder skrives kun af developer, som aldrig retter i definitionen ovenfor.>

### Hvad er lavet
Commits på grenen: `e77cb29` (upload) og `fa3efe9` (undtagelser).

Upload:
- `koersel/models.py`: `Koersel` har to nye valgfrie felter, `uploadet_af` (bruger, `SET_NULL`, `related_name="+"` fordi `oprettet_af` allerede peger på brugeren) og `uploadet` (tidspunkt). Migrering `koersel/migrations/0002_koersel_uploadet_af_og_tidspunkt.py`, lavet med `makemigrations`. Eksisterende kørsler får tomme felter.
- `koersel/services.py`: `opret_linjer` tager en valgfri `bruger` og sætter `uploadet_af` og `uploadet` samme sted som `filnavn`, inde i samme transaktion. En afvist upload når aldrig dertil, så felterne ændres ikke.
- `koersel/views.py` (`upload`): sender `request.user` med.
- `templates/koersel/upload.html`: "Sidst uploadet: filnavn, af brugernavn, dd.mm.åååå kl. tt:mm". Brugernavn (`get_username`) vises kun hvis brugeren findes; tidspunktet kun hvis det er sat (ældre kørsler viser kun filnavnet). Uden fil står der stadig "Ingen fil valgt". Dashboard og Gennemse er urørt.
- Færdig-når for upload (alle fem punkter) er dækket af tests i `koersel/tests.py`: `test_upload_gemmer_hvem_og_hvornaar_og_viser_det`, `test_ny_upload_erstatter_fil_bruger_og_tidspunkt`, `test_afvist_upload_aendrer_ikke_sidst_uploadet`, `test_koersel_uploadet_foer_felterne_viser_kun_filnavn`, `test_slettet_bruger_viser_filnavn_og_tidspunkt_uden_navn`, `test_uden_upload_staar_der_ingen_fil_valgt`.

Undtagelser:
- `static/js/undtagelser.js`: ny `visFoersteManglende()` finder første række hvis statusmærke ikke er `ok` (altså ud fra den eksisterende statusudregning i `opdater()`), sætter klassen `mangler` på rækken og ruller den til midten af vinduet (`scrollIntoView`, uden animation hvis brugeren har bedt om mindre bevægelse). Kaldes når "Beregn" afbrydes lokalt, og ved indlæsning hvis formularen bærer `data-afvist`. Markeringen fjernes ved enhver ændring i formularen (`input`-hændelse); derefter udregnes status som før. Meddelelsen om hvor mange der mangler er uændret, og afbrydelsen er uændret. Reglerne for hvornår en række er klar er ikke rørt.
- `koersel/views.py` (`undtagelser`): ved afvisning fra serveren (`BeregningsFejl`) sættes `afvist`, og første række med fejl (`foerste_mangler`) sendes til skabelonen.
- `templates/koersel/undtagelser.html`: formularen får `data-afvist="1"` efter afvist beregning; den første manglende række får klassen `mangler` fra serveren, så markeringen også er der uden at JS kører.
- `static/css/app.css`: `.row.mangler` (gul baggrund, rød kant og rød streg i venstre side).
- Tests i `koersel/tests.py`: `test_afvist_beregning_markerer_foerste_manglende_raekke` (afvist beregning bærer `data-afvist` og præcis én markeret række, den første der mangler, ikke den næste; meddelelsen og "1 af 3 klar" er uændrede), `test_undtagelser_uden_afvisning_har_ingen_markering` og `test_gem_kladde_med_manglende_raekke_markerer_ikke`. At beregningen kører uden markering når alle er klar, dækkes af den eksisterende `test_hele_flowet_beregn_pdf_godkend_eksport`.

Fælles:
- Ingen filter, søgning, nye skærme eller nye knapper. Ingen nye pakker. Ingen nye kommandoer eller indstillinger.
- Kørt: `manage.py test koersel register` (30 grønne) og `manage.py makemigrations --check` (ingen ændringer). Hele suiten er ikke kørt, som aftalt. `node --check` på JS-filen er ren. Der er ingen linter sat op.
- Til README, hvis architect vil: upload-skærmen viser nu hvem der uploadede og hvornår; Undtagelser ruller til og markerer første række der mangler noget, når man trykker Beregn.

### Hvad er ikke lavet, og hvorfor
- **Ikke efterprøvet i en browser** (agenter må ikke starte en). Det gælder: at siden faktisk ruller til rækken, at rulningen sker efter serverafvisning ved indlæsning, at markeringen ser tydelig ud (farver, i både lys og mørk tilstand), og at den forsvinder når brugeren retter noget. Det der er prøvet maskinelt, er HTML'en fra serveren (`data-afvist`, klassen `mangler` på den rigtige række) og at JS-filen er syntaktisk gyldig. JS-logikken selv er ikke kørt.
- Ellers intet.

### Uklart
- Skærmbilledet efter serverafvisning: markeringen er både sat af serveren og af skærmkoden (samme række, samme regel). Jeg valgte det, så markeringen også er der uden JS, og så der er noget at teste. Siger du nej til dobbeltheden, kan serverens klasse fjernes uden at rulningen ændres.
- Afvises beregningen kun med generelle fejl, er `data-afvist` sat, men ingen række er ikke-klar, så der sker ingen rulning eller markering (som besluttet). Intet at afgøre; nævnt for fuldstændighedens skyld.
- Intet andet.
