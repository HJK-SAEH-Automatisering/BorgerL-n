---
nummer: task-0001
titel: Tydeligere kørselsskærme: sidst uploadet og første manglende række
status: planlagt
kilde: mockup-0002, mockup-0004
oprettet: 2026-10-22
---

# task-0001 — Tydeligere kørselsskærme: sidst uploadet og første manglende række

## Hvad og hvorfor
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
intet

## Beslutninger
- BESLUTTET: Felter på kørslen frem for opslag i auditloggen — auditloggen er fri tekst og ikke stedet at hente visningsdata fra. Afvist: opslag på handlingsteksten "Uploadede timefil".
- BESLUTTET: Én opgave for de to ændringer — hver for sig er for lille til at bære en tråd, og begge ligger i kørselsskærmene. Afvist: to opgaver.
- BESLUTTET: Ingen filter "vis kun dem der mangler" på Undtagelser — rulning til første række løser det samme uden et nyt kontrolelement. Se beslutningsloggen.
- BESLUTTET: Dashboard og Gennemse transport uændrede — kun upload-skærmen har brug for at vide hvad der overskrives.

## Åbne punkter
intet

## Indvendinger
<Udfyldes af andre roller.>

---

## Developers noter

<Alt over denne overskrift ejes af architect. Alt herunder skrives kun af developer, som aldrig retter i definitionen ovenfor.>

### Hvad er lavet
### Hvad er ikke lavet, og hvorfor
### Uklart
