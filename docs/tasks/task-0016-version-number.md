---
nummer: task-0016
titel: Indfør versionsnummer 0.1.0, vist i bunden af skærmene og gemt i hver beregning
kilde: interview
status: i-gang
oprettet: 2026-11-09
---

# task-0016 — Indfør versionsnummer 0.1.0, vist i bunden af skærmene og gemt i hver beregning

## Hvad og hvorfor
Appen har intet versionsnummer. Før den første udrulning skal der være ét, så en bruger kan oplyse, hvilken udgave de bruger, når de melder en fejl, og så en gemt beregning kan fortælle, hvilken udgave der lavede den. Reglerne i beregningsmotoren kommer til at ændre sig, og snapshottet er beviset på en udbetaling. Nummeret starter på 0.1.0.

## Færdig når
- [ ] Versionsnummeret står ét sted i koden, og det er 0.1.0.
- [ ] I bunden af alle skærme, der bruger den fælles grundskabelon, står en lille tekst med appens navn og nummeret: "MedarbejderLøn 0.1.0". Teksten er diskret og ændrer ikke, hvordan skærmene ser ud ellers, og den kommer ikke til at skubbe knapper eller rækker.
- [ ] Teksten står også på loginsiden, hvis den bruger grundskabelonen; ellers behøver den ikke.
- [ ] Når "Beregn" trykkes, gemmes versionsnummeret i beregningens snapshot under nøglen `app_version`. Den findes ud over de nøgler, der er der i dag, og ingen af dem ændres. Snapshottets egen `version` (formatet) og `rapport_layout` er uændrede.
- [ ] PDF-rapporten er uændret og viser ikke nummeret. `LAYOUT_VERSION` er uændret. En gemt rapport kan stadig kontrolleres med `manage.py verificer_rapport`, og en ny beregnings rapport er identisk med en, der ville være lavet før opgaven.
- [ ] Gamle beregninger uden `app_version` fungerer som før og ændres ikke.
- [ ] README og CLAUDE.md fortæller, hvor nummeret står, og at det kun skiftes ved en udrulning, efter at mennesket har bedt om det: nye funktioner hæver midterste del (0.2.0), rettelser sidste del (0.1.1), og 1.0.0 er den første udgave, der bruges rigtigt i drift.
- [ ] Der er tests: bunden af en skærm viser "MedarbejderLøn 0.1.0", en ny beregning har `app_version` i snapshottet og den samme værdi som nummeret i koden, en gammel beregning uden nøglen kan stadig vises og kontrolleres, og PDF'ens indhold og layoutversion er uændrede.
- [ ] Testsuiten er grøn.

## Sådan bygger vi det
- **Ét sted.** En konstant i `config` (fx `APP_VERSION = "0.1.0"` i `config/settings.py`) er kilden. Skabeloner og snapshot læser den derfra, og der skrives ikke nummeret andre steder. Er der en bedre plads i koden, vælger developer den og skriver det i noterne.
- **Bunden af skærmene.** `templates/base.html` får en lille linje nederst, der viser appens navn og nummeret. Skabelonen får nummeret via en kontekstbehandler (`context_processors` i `config/settings.py`), så ingen visning skal sende det med. Udseendet følger de eksisterende stilarter i `static/css/app.css`; kun en meget lille ny stil, hvis det er nødvendigt (afsnit i bunden, mindre og dæmpet tekst).
- **Snapshot.** `koersel/services.py` tilføjer `app_version` til snapshottet, der hvor det bygges. Intet andet i snapshottet ændres, og PDF'en læser ikke nøglen.
- **Dokumentation.** README (afsnittet til dem, der driver appen) og CLAUDE.md får en kort omtale. README skrives i almindeligt dansk.
- **Ingen ny model og ingen migrering.** Snapshottet er data, der allerede gemmes frit.

## Hvad vi ikke rører
- Beregningsmotoren, reglerne og tallene.
- PDF-rapportens indhold og layout, `LAYOUT_VERSION` og snapshottets formatversion.
- Eksportens indhold.
- Gamle gemte beregninger.
- Et automatisk versionsskifte, git-tags og en udrulningsproces. Nummeret skiftes i hånden, når mennesket beder om det.

## Afhænger af
intet

## Beslutninger
- BESLUTTET: Nummeret vises i bunden af alle skærme som en lille tekst — mennesket besluttede det, så en bruger kan oplyse udgaven uden at spørge den, der driver appen. Afvist: kun at have det i koden og README.
- BESLUTTET: Nummeret gemmes i hver beregnings snapshot, men står ikke på PDF'en — mennesket besluttede det. Snapshottet er beviset på en beregning, og et senere nummer kan ikke sættes på beregninger, der allerede er lavet. Afvist: at lade snapshottet være uændret; at ændre rapportens layout.
- BESLUTTET: Nummeret skiftes kun ved en udrulning, når mennesket beder om det — mennesket besluttede det. Afvist: at hæve det automatisk for hver afsluttet opgave, fordi det vokser hurtigt og intet siger om, hvad der er rullet ud.
- BESLUTTET: Nøglen i snapshottet hedder `app_version`, for ikke at forveksle den med snapshottets egen `version`, som er formatet — architects valg, kan ændres.

## Åbne punkter
intet

## Indvendinger
<Udfyldes af andre roller.>

## Developers noter

### Hvad er lavet
- `config/settings.py`: konstanten `APP_VERSION = "0.1.0"` er det eneste sted, nummeret står. Kontekstbehandleren er føjet til `TEMPLATES`.
- `config/context_processors.py` (ny): `app_version` giver skabelonerne `APP_VERSION`, så ingen visning sender det med.
- `templates/base.html`: nederst en linje `MedarbejderLøn {{ APP_VERSION }}` efter `.side`-blokken, så den ikke ligger i trinsøjlens grid og ikke skubber knapper eller rækker. Loginsiden bruger grundskabelonen og viser den også.
- `static/css/app.css`: én ny stil, `.appversion` (lille, dæmpet, centreret tekst med afstand).
- `koersel/services.py`: `"app_version": settings.APP_VERSION` i snapshottet, lige efter `rapport_layout`. `version`, `rapport_layout` og de øvrige nøgler er uændrede. `LAYOUT_VERSION` og `beregning/pdf.py` er ikke rørt; PDF'en læser ikke nøglen. Ingen model, ingen migrering.
- `koersel/tests.py` (fire nye tests i `FlowTests`): bunden af dashboard, medarbejderliste og login viser "MedarbejderLøn 0.1.0"; ny beregning har `app_version` lig `settings.APP_VERSION`, og nøglesættet er det gamle plus `app_version`; en beregning hvor nøglen er fjernet kan vises (rapport og godkend) og kontrolleres med `verificer_rapport`; PDF er byte-identisk med og uden nøglen, matcher det gemte SHA-256, `LAYOUT_VERSION` er 2, og nummeret står ikke i PDF-teksten.
- `CLAUDE.md`: nyt afsnit `## Versionsnummer` (hvor nummeret står, at det kun skiftes ved udrulning efter menneskets ønske, og reglen for 0.2.0 / 0.1.1 / 1.0.0).
- Testsuiten: `.venv\Scripts\python.exe manage.py test` kørt én gang til sidst, 139 tests, OK (135 før plus de fire nye). Ingen linter er sat op.
- Nyt for brugere, til README: bunden af hver skærm (også loginsiden) viser "MedarbejderLøn 0.1.0", så en bruger kan oplyse udgaven ved en fejlmelding. Til dem der driver appen: nummeret står i `config/settings.py` som `APP_VERSION`, og hver ny beregnings snapshot gemmer det som `app_version`. Ældre beregninger har ikke nøglen og er uændrede. Nummeret skiftes kun ved en udrulning, når mennesket har bedt om det (nye funktioner 0.2.0, rettelser 0.1.1, 1.0.0 er første udgave i rigtig drift).

### Hvad er ikke lavet, og hvorfor
- README: opgaven kræver en omtale, men README er `architect`s og må ikke rettes af mig. Teksten til den står i sidste punkt under "Hvad er lavet".
- Udseendet i en browser er ikke efterprøvet (ingen browser må startes af en agent). Det er kun efterprøvet, at teksten står i HTML'en. At linjen er diskret og ikke skubber noget, bør `architect` eller mennesket se på en skærm.

### Uklart
intet
