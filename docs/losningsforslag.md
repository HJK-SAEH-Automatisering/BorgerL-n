# Erstatning af "VIKA løn og kørsel" – løsningsforslag

## Status

Dette dokument beskriver reglerne, designet og de beslutninger, webappen er bygget efter. Se
"Status og næste skridt" nederst for hvad der er bygget, og hvad der mangler før produktion.

## Kontekst

Hjørring Kommune administrerer i dag §103 SEL (beskyttet beskæftigelse) og den tilhørende
§105 SEL-befordringsgodtgørelse i et stort, manuelt vedligeholdt Excel-ark ("VIKA løn og
kørsel.xlsx"). Arket indeholder borgernes CPR-numre, adresser og arbejdssted, og beregner
hver måned arbejdsdusør og kørselstilskud/-træk via indlejrede, uigennemsigtige Excel-formler
(nested IF/VLOOKUP på tværs af 6 faneblade). Data om timer kommer i dag fra et andet system
(eksemplificeret ved "eksempel data.xlsx": navn + timer i formatet t:mm), og
tastes/kopieres manuelt ind.

Formålet med den nye løsning er at:
- Fjerne CPR/borgerdata fra ustrukturerede Excel-ark på skrivebord/OneDrive.
- Gøre beregningsreglerne gennemsigtige og testbare for nye administrative medarbejdere.
- Minimere den månedlige administration.
- Sikre lovmedholdelighed (§103/§105 SEL) og et revisionsspor for beregningerne.

### Beslutninger truffet

- **Platform:** Skræddersyet webapp (ikke Power Platform, ikke et eksisterende fagsystem).
- **Ejerskab:** Bygges og driftes af brugeren selv, med hjælp fra Claude Code.
- **Dataintegration:** Timedata indlæses fortsat som en fil hver måned (som i dag), men selve
  beregningen, opslag og validering automatiseres herfra.
- **Borgerregister:** Systemet skal have sit **eget borgerregister**, som administrative
  medarbejdere selv kan vedligeholde i webappen – de skal kunne **oprette nye borgere samt
  rette adresser og andre relevante personoplysninger** direkte i løsningen. Der findes ikke
  en afklaret ekstern autoritativ datakilde til CPR/adresser endnu, så admin skal ikke stå
  uden mulighed for at indtaste/rette data i mellemtiden. Medarbejdernummer/"Tj.nr." bruges
  som stabilt, ikke-følsomt internt ID i systemets eget register, når en borger først er
  oprettet. Den månedlige timefil indeholder hverken CPR eller Tj.nr. – kun navn – så
  matchningen fra timefil til borger sker på **navn** (se regel om Import nedenfor), mens
  selve personoplysningerne (CPR, navn, adresse) opbevares i systemets eget register – med
  tilhørende adgangsstyring og logning (se "Sikkerhed & GDPR"). En senere
  integration til en autoritativ ekstern kilde (fx CPR-registret) kan tilføjes som en
  opslags-/valideringsfunktion oven på registret, men er ikke en forudsætning for første
  version.
- **Webapp og database:** Det bliver en webapp (Django). SQLite bruges under udvikling og indtil
  webappen er godkendt af brugeren og kollegerne; produktion kører på MSSQL. Skiftet sker kun
  via konfiguration (se README).
- **Kildesystem:** Timefilen kommer fra Punchly og indeholder kun navn og timer.
- **PDF-rapport ved hver beregning:** Hver gang beregningen køres, gemmes et uforanderligt
  snapshot og en PDF-rapport, der i detaljer specificerer udregningen for hver borger (uden
  CPR og adresse), så man senere kan se, hvordan en udbetaling er nået frem. Gamle rapporter
  slettes aldrig.
- **Godkendelse:** Webappen laver beregningerne, men intet må sendes videre (fx til
  lønudtræk), før en administrativ medarbejder eksplicit har godkendt beregningen. I denne
  proces skal det være fuldt gennemsigtigt, hvordan beregningen er lavet for hver enkelt
  borger – ikke kun slutbeløbet.

## Regler udtrukket af det eksisterende ark

Ved at læse rå-XML'en og formlerne i "VIKA løn og kørsel.xlsx" (faneblade
"Indberetningsliste", "Dobbeltansættelse", "Zone priser", "Afdelinger", "Mail fra Jurist",
"Pjecen") er reglerne kortlagt sådan:

1. **Arbejdsdusør (lønart 110):** `timer × sats pr. time` = løn før skat. Løn efter skat =
   løn før skat minus `trækprocent` (i eksemplet 40 %), nedrundet til hele kroner.
2. **Befordring, hovedregel (§105 SEL, jf. jurist-mail 27.03.2023):** Borgeren skal selv
   betale transport inden for 10 km / 2 zoner ("Afstandskrav" = 10 km, konfigurerbart).
   Denne egenbetaling må dog **aldrig overstige 30 %** af borgerens løn efter skat
   ("Maks kørselstræk" = 30 %, konfigurerbart). Egenbetalingen er den mindste af: zoneprisen
   for borgerens antal zoner, og 30 % af løn efter skat.
3. **Befordringsudbetaling ud over 2 zoner:** Hvis zoneprisen for borgerens faktiske zoner er
   højere end maks-egenbetalingen, betaler kommunen differencen (kørselsudbetaling, lønart
   991).
4. **Individuel beregning (prioritet 1):** Hvis markeret ("skriv 1"), beregnes
   kørselstilskuddet i stedet som `2 × kontantpris (barn/67) × antal fremmødedage i måneden`
   minus egenbetalingen (formlen i "Indberetningsliste") – bruges til særlige/individuelle sager
   og overstyrer standardberegningen. **Uafklaret:** fanebladet "Dobbeltansættelse" viser
   bruttobeløbet uden fradrag af egenbetaling (se eksemplet nedenfor). Webappen følger
   formlen i "Indberetningsliste", men punktet bør bekræftes af en fagperson.
5. **TAXA-spor:** Hvis borgeren er bevilget TAXA, følger beregningen en anden gren
   (afkrydset felt), adskilt fra "kører selv"-sporet.
6. **Zonepriser (NT-takster):** Ekstern, årligt opdateret referencetabel (antal zoner →
   pris). Bemærk: beregningen bruger konsekvent **børne/67-taksten** (den reducerede takst),
   ikke voksentaksten – formentlig fordi målgruppen typisk er berettiget til denne takst.
   Dette bør bekræftes, men skal under alle omstændigheder bevares som en eksplicit,
   admin-redigerbar og **versioneret** opslagstabel i den nye løsning (ikke hardcodet), da
   priserne ændres 1. januar hvert år.
7. **Dobbeltansættelse:** Et separat regneark bruges i dag til manuelt at holde øje med
   borgere med flere ansættelser (for at undgå dobbelt udbetaling) – bør erstattes af en
   automatisk kontrol i den nye løsning.
8. **Afdeling → lønseddelmodtager:** Simpel opslagstabel der styrer, hvem der skal
   modtage/behandle den enkelte borgers lønseddel (intern rutning, ikke lovgivning).
9. **Kendte fejltilstande i dag:** Det eksisterende ark indeholder synlige `#N/A`-fejl og
   prompt-tekster i talceller ("INGEN ZONE ANGIVET", "TAXA/KØRSEL?", "UDFYLD 'KØRER SELV' OG
   'ZONER'") når påkrævede felter ikke er udfyldt. Den nye løsning skal håndtere disse som
   eksplicitte, synlige valideringsfejl i godkendelsesskærmen – ikke som formel-outputs, der
   kan forveksles med rigtige tal.

### Konkrete eksempler fra det nuværende ark (bekræfter reglerne)

- **Individuel beregning:** En borger med 13,2 km til arbejde (zone 3), markeret til
  individuel beregning med 4 fremmødedage i måneden. Kontantprisen (barn/67) for zone 3 er
  17 kr. Bruttobeløbet `2 × 17 × 4 = 136 kr` er præcis den værdi, der står i kolonnen "Udgift
  pr. måned" i fanebladet "Dobbeltansættelse". Formlen for selve udbetalingen i
  "Indberetningsliste" trækker derudover borgerens egenbetaling fra (regel 4 ovenfor).
- **Manglende data giver i dag stiltiende fejl, ikke en tydelig advarsel:** En borger med
  44,2 registrerede timer (884 kr i løn før skat, 531 kr efter skat), hvor hverken "TAXA"
  eller "Kører selv" er afkrydset, og zonen ikke er udfyldt. Arket viser i dag blot teksterne
  "INGEN ZONE ANGIVET" og "UDFYLD ''KØRER SELV'' OG ''ZONER''" i outputcellerne – uden at
  standse processen eller advare tydeligt. Dette er nøjagtigt den type sag, hvor den nye
  løsnings godkendelsesskærm skal blokere med en klar fejlmelding, i stedet for at lade en
  ufuldstændig beregning glide videre.

Disse regler er ret specifikke for §103/§105-området og bør **valideres med en jurist/
fagperson**, før de kodes 1:1 – dels fordi nuværende formler tydeligvis allerede fejler i
kanttilfælde, dels fordi reglerne bør dokumenteres med lovhenvisning i selve koden.

## Anbefalet arkitektur

**Stack** (valgt for at kunne vedligeholdes af én person med hjælp fra Claude Code, uden et
stort IT-drift-apparat):
- Backend: Python + Django (indbygget admin, auth, ORM – giver en solid UI til at
  vedligeholde zonepriser, afdelinger og regelparametre uden et separat frontend-projekt).
- Database: PostgreSQL (SQLite kan bruges i en tidlig prototype).
- Frontend: Server-renderede Django-templates + HTMX til de interaktive dele (undgår en tung
  JS-stack, som er sværere at vedligeholde alene).
- Godkendelse/login: anbefales integreret med kommunens Entra ID/AD, så der ikke opfindes en
  ny brugerdatabase til følsomme data – kræver sandsynligvis IT/digitalisering som
  interessent for hosting og login, selvom udvikling sker selv (se "Åbne punkter" nedenfor).

**Kernemoduler:**

1. **Import** – upload af den månedlige timefil (som "eksempel data.xlsx"), parses og
   matches til kendte borgere **på navn**, da timefilen hverken indeholder CPR eller Tj.nr.
   Navnematch er i sagens natur skrøbeligt (stavevarianter, navnesammenfald, navneskift) –
   uafklarede eller flertydige rækker ("ny medarbejder", "fratrådt medarbejder", flere
   borgere med samme navn) vises derfor altid til manuel bekræftelse/afklaring i importtrinet
   i stedet for at blive gættet automatisk eller forsvinde i en celle.
2. **Stamdata** – Afdelinger, zonepriser (versioneret), regelparametre (afstandskrav,
   maks-procent) – alt admin-redigerbart med historik, så en ændring 1. januar ikke kræver
   en kodeændring.
3. **Beregningsmotor** – rene, enhedstestede funktioner der implementerer reglerne ovenfor,
   med docstrings der refererer til §103/§105 SEL og til jurist-mailen. Erstatter de
   indlejrede formler med læsbar, versioneret kode. For hver borger returnerer motoren ikke
   kun slutresultatet, men også et struktureret **beregningsgrundlag** (hvilket spor der er
   brugt – standard/individuel/taxa, samt hver mellemregning: timer × sats, løn før/efter
   skat, borgerens zone og zonepris, maks-egenbetaling, faktisk egenbetaling og evt.
   kørselsudbetaling). Dette grundlag er det, der vises til den administrative medarbejder i
   godkendelsesskridtet, så det til enhver tid er gennemsigtigt *hvorfor* et bestemt beløb er
   nået frem til for netop denne borger.
4. **Borgerregister** – CRUD-skærmbilleder hvor administrative medarbejdere kan oprette nye
   borgere og rette CPR, navn, adresse, arbejdssted og andre relevante personoplysninger.
   Erstatter dagens manuelle indtastning direkte i regneark-celler med en struktureret,
   valideret formular og et revisionsspor over ændringer. Bygges med et abstraheret
   opslagsinterface (`BorgerLookupProvider`), så en fremtidig integration til en autoritativ
   ekstern kilde (fx CPR-registret) senere kan bruges til at validere/udfylde felter uden at
   ændre resten af systemet.
5. **Gennemgang & godkendelse** – obligatorisk step efter beregning: hver borgers resultat
   vises sammen med det fulde beregningsgrundlag fra beregningsmotoren (jf. punkt 3), så det
   er klart *hvordan* beløbet for netop denne borger er beregnet, samt evt. advarsler
   (manglende zone, dobbeltansættelse, ny/fratrådt medarbejder). En administrativ medarbejder
   skal eksplicit godkende beregningen (pr. borger og/eller for hele månedens kørsel samlet),
   før noget går videre. Uden denne godkendelse forbliver kørslen i status "afventer
   godkendelse" og kan hverken eksporteres eller på anden måde sendes videre.
6. **Eksport** – kan først køre for en given måned, når alle linjer er godkendt i trin 5.
   Genererer lønudtræk (lønart 110 og 991) pr. afdeling/lønseddelmodtager, baseret på
   borgerregisterets aktuelle data.
7. **Audit log** – hvem har set/ændret personoplysninger, stamdata, regler og godkendelser,
   og hvornår – vigtigt både for gennemsigtighed og fordi registret selv opbevarer CPR.

**Dataflow pr. måned:** Upload timefil → match til medarbejdere → admin udfylder evt.
undtagelser (taxa/individuel/kører selv) → beregningsmotor kører og producerer resultat +
beregningsgrundlag pr. borger → gennemgangsskærm med fuld gennemsigtighed i beregningen samt
advarsler → **eksplicit godkendelse er en hård spærre** – intet eksporteres eller sendes
videre for en borger/måned, før en administrativ medarbejder har godkendt → lønudtræk
genereres.

## Udrulning / validering

Byg beregningsmotoren først og valider den mod det nuværende arks egne resultater (som
eksemplerne ovenfor) for en håndfuld borgere, før noget andet bygges. Kør evt. den nye
løsning parallelt med Excel-arket i 1-2 måneder, før arket lægges endeligt ned.

## Sikkerhed & GDPR

- Systemet er dataansvarligt for CPR/personoplysninger, da de indtastes og opbevares direkte
  i borgerregistret. Det kræver adgangsstyring (kun relevante administrative medarbejdere),
  kryptering, logning af opslag/ændringer og en klar sletning/opbevaringspolitik.
- Bør afklares med IT/digitalisering/DPO før produktionssætning, uanset at udviklingen sker
  selv.

## Åbne punkter / risici

- **Hosting og login** kræver formentlig IT/digitalisering, selvom udvikling sker selv, da
  løsningen håndterer økonomiske data og CPR-numre om udsatte borgere.
- **Retlig validering** af den udtrukne regelbeskrivelse ovenfor bør ske med en fagperson/
  jurist, da nuværende ark har synlige fejltilstande, der tyder på at reglerne allerede i dag
  ikke håndteres 100 % korrekt i alle kanttilfælde.
- Den reducerede takst ("børne/67") brugt i alle formler bør bekræftes som tilsigtet, ikke en
  fejl i det oprindelige ark.
- Kildesystemet for timedata (der leverer filer som "eksempel data.xlsx") er ikke undersøgt
  for evt. API – kan genovervejes senere, da bruger har valgt manuel fil for nu.
- **Navnematch ved import er en risiko:** Da timefilen ikke indeholder CPR eller Tj.nr., skal
  hver måneds rækker matches på navn alene. To borgere med samme eller lignende navn kan
  forveksles. Importtrinet skal derfor altid vise usikre/flertydige match til manuel
  godkendelse, aldrig auto-vælge ved tvivl.

## Status og næste skridt

Første version af webappen er bygget: borgerregister, stamdata, beregningsmotor med
beregningsgrundlag, import af Punchly-filen, de fire skærme (upload, gennemse transport,
undtagelser, godkend), PDF-rapport ved hver beregning, spærret CSV-eksport og auditlog. Se
[README](../README.md) for opstart. Den kører på SQLite; MSSQL er konfigureret, men ikke afprøvet.

Før produktion:

1. Bekræft regelbeskrivelsen med en fagperson/jurist – især regel 4 (fradrag af egenbetaling
   ved individuel beregning), regel 6 (reduceret takst) og afrundingen af egenbetalingen (rundes
   ned til øre) og skattetrækket (rundes ned til hele kroner).
2. Afprøv importen på en rigtig Punchly-eksport (kun layoutet i "eksempel data.xlsx" er testet).
3. Afklar hosting, login (Entra ID) og opbevaringspolitik for CPR og PDF-rapporter med
   IT/digitalisering og DPO.
4. Afprøv MSSQL og kør parallelt med Excel-arket i 1-2 måneder.
