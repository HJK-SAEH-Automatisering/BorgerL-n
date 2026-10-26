---
nummer: task-0007
titel: Skift ordet borger til medarbejder, og navnet BorgerLøn til MedarbejderLøn
kilde: interview
status: planlagt
oprettet: 2026-10-26
---

# task-0007 — Skift ordet borger til medarbejder, og navnet BorgerLøn til MedarbejderLøn

## Hvad og hvorfor
Mennesket vil ikke, at appen siger "borger". Personerne skal hedde "medarbejder" overalt, hvor nogen læser det, fx "Medarbejderregister" i stedet for "Borgerregister". Appens synlige navn skifter fra "BorgerLøn" til "MedarbejderLøn". Opgaven ændrer kun det, der kan læses. Navne i koden, tabeller, adresser i browseren, mappen og repoet på GitHub bliver, som de er.

## Færdig når
Skærmene:

- [ ] Ingen skærm viser længere ordet "borger" i nogen form, hverken i topbjælke, menuer, overskrifter, knapper, tabeloverskrifter, meddelelser, fejl, hjælpetekster, formularfelter, tomme tilstande eller advarsler. "Borgere" er blevet til "Medarbejdere", "borgerens" til "medarbejderens", og "Borgerregister" til "Medarbejderregister". Bøjninger og sammensatte ord følger med.
- [ ] Appens synlige navn er "MedarbejderLøn" i topbjælken, i sidernes titler og på loginsiden.
- [ ] Administrationssiden viser medarbejder og medarbejdere i stedet for borger og borgere, også i overskrifter og feltnavne.

Rapporter og eksport:

- [ ] Nye PDF-rapporter og nyt lønudtræk (CSV) bruger ordet "medarbejder" og navnet "MedarbejderLøn", hvor ordet i dag står.
- [ ] Allerede gemte PDF-rapporter er uændrede, og kontrollen af en gemt rapport virker stadig for dem.

Dokumenter:

- [ ] `README.md`, `CLAUDE.md` og `docs/losningsforslag.md` bruger "medarbejder" og "MedarbejderLøn". `CLAUDE.md` og `README.md` nævner, at mappen og repoet stadig hedder BorgerLøn.
- [ ] Skitserne under `docs/mockups/`, beslutningsloggen, de afsluttede opgaver og testrapporterne er uændrede. De er historik.

Uændret:

- [ ] Gemte data virker uændret. Eksisterende kørsler, medarbejdere og rapporter kan åbnes som før.
- [ ] Alle adresser i browseren er uændrede.
- [ ] Beregningen giver de samme beløb som før.

Fælles:

- [ ] Tests, der kontrollerer tekster, er rettet til de nye ord. Der er en test, der viser, at ingen af skærmene indeholder "borger" i det synlige indhold.
- [ ] Testsuiten er grøn.

## Sådan bygger vi det
- **Skel mellem tekst og navne i koden.** Ordet står mange steder i koden som navne på variabler, klasser og funktioner. Dem rører vi ikke. Kun tekst, brugeren kan læse: skabeloner, meddelelser og fejl i visningerne og formularerne, hjælpetekster og feltnavne, visningsnavne i administrationen (`verbose_name`), advarsler fra beregningen, rapportens og eksportens tekster, og skærmkodens tekster.
- **Navne og adresser bliver.** Modellernes navne, tabellerne, adressernes sti og navne, og eksisterende migreringer ændres ikke. Ændrede visningsnavne giver en ny migrering uden betydning for data; den laves med `makemigrations`.
- **PDF-rapporten.** Ordene ændres i `beregning/pdf.py`. Står der et layoutnummer, som skal øges, når rapportens tekst ændres, øges det, og det skrives i noterne. Allerede gemte PDF-filer ændres aldrig.
- **Grammatik.** Ordene følger dansk: "en medarbejder", "medarbejderen", "medarbejdere", "medarbejdernes", "medarbejderens", "medarbejderregistret".
- **Navnet.** "BorgerLøn" skifter til "MedarbejderLøn" i det synlige. Mappen, repoet, `.claude/launch.json` og kodens navne bliver.
- **Søgning til sidst.** Udvikleren søger efter ordet i skabeloner, tekster i koden og dokumenterne og skriver i sine noter, hvad der er tilbage, og hvorfor det er et navn i koden.

## Hvad vi ikke rører
- Navne i koden, modellernes navne, tabeller og eksisterende migreringer.
- Adresser i browseren.
- Beregningsmotorens regler og beløb.
- Mappen og repoet på GitHub.
- Skitserne, beslutningsloggen, afsluttede opgaver og testrapporter.
- Demodataenes fiktive navne.

## Afhænger af
task-0006 — begge ændrer Godkend-skærmen og de tests, der kontrollerer dens tekster. Der bygges kun på én opgave ad gangen, og denne sendes først af sted, når task-0006 er afsluttet.

## Beslutninger
- BESLUTTET: Kun synlig tekst ændres — navne i koden, tabeller og adresser bliver. En omdøbning af dem er en stor og risikabel ændring uden gevinst for brugerne. Afvist: omdøbning af modeller, tabeller og adresser.
- BESLUTTET: Det synlige navn skifter til "MedarbejderLøn" — mennesket valgte det, fordi navnet indeholder ordet. Mappen og repoet bliver. Afvist: at omdøbe repoet nu.
- BESLUTTET: Gemte PDF-rapporter ændres ikke — den gemte PDF er selve beviset på en beregning.
- BESLUTTET: `README.md`, `CLAUDE.md` og `docs/losningsforslag.md` rettes, men skitser, beslutningslog, afsluttede opgaver og testrapporter gør ikke — de er historik.

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
