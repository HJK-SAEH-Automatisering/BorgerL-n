# Beslutningslog

Append-only. Nyeste øverst. Én linje pr. beslutning.

**Ejes af `architect`.** Dens tråd er den eneste samtale i modellen, og loggen er det eneste spor af den der overlever tråden. Hver beslutning truffet i en `architect`-tråd skrives ind, med begrundelse, før tråden lukkes.

Her hører også **afvisninger**: et fund der ikke bliver en opgave, skal have sin begrundelse her. Ellers er det et fund der forsvandt.

`Nr.` er nummeret beslutningen hører til — `task-0042`, `test-0003` — eller `—` hvis den gælder projektet som helhed.

| Dato | Nr. | Beslutning | Begrundelse | Rolle |
|---|---|---|---|---|
| 2026-10-22 | task-0001 | Opgaven samler "Sidst uploadet" (mockup-0002) og rulning til første manglende række (mockup-0004). Felter på kørslen frem for opslag i auditloggen | Hver for sig er de for små til at bære en tråd, og begge ligger i kørselsskærmene. Auditloggen er fri tekst og skrøbelig at slå op i | architect |
| 2026-10-22 | mockup-0004 | Synlig bekræftelse af "Gem kladde" afvist. Findes allerede | Siden viser i dag "Kladden er gemt." efter gem, og gemningen logges. Intet at bygge. Besluttet af architect, kan vendes. Skitsen er hermed behandlet | architect |
| 2026-10-22 | mockup-0004 | Filter "vis kun dem der mangler" på Undtagelser afvist | Rulning til første række løser det samme uden et nyt kontrolelement. Besluttet af mennesket sammen med forrige linje | architect |
| 2026-10-22 | mockup-0004 | "Beregn" på Undtagelser ruller til første række, der mangler noget, og markerer den. Bliver task-0001 | Brugeren slipper for at lede efter rækkerne. Det er lidt skærmkode og ingen ændring i data. Besluttet af mennesket | architect |
| 2026-10-22 | mockup-0003 | Søgning og filter i listen på Gennemse transport afvist. Skitsen er hermed behandlet og gav ingen opgaver | Ved omkring 50 rækker finder browserens egen søgning et navn med det samme. Det kræver ekstra skærmkode uden et behov i dag. Besluttet af mennesket | architect |
| 2026-10-22 | mockup-0003 | Rækker med samme navn flere gange i filen vises fortsat hver for sig med en markering. De lægges ikke sammen | Markeringen er det, der får beregningen til at behandle borgeren som dobbeltansat. Sammenlægning ville skjule dobbeltansættelsen. Besluttet af architect, kan vendes | architect |
| 2026-10-22 | mockup-0003 | Ændring af afstand og transport på Gennemse transport gemmes fortsat i borgerregisteret og gælder altid. Undtagelser for kun én måned rettes i Undtagelser | Skærmen siger det selv, og trinnet efter findes netop til rettelser, der kun gælder måneden. Afstand er en egenskab ved borgeren. Besluttet af architect, kan vendes | architect |
| 2026-10-22 | mockup-0002 | "Sidst uploadet" på upload-skærmen skal vise navn, dato og klokkeslæt, ikke kun filnavn. Bliver en opgave | Uploades en ny fil, erstattes rækker og rettelser; brugeren skal kunne se, hvad der overskrives. Navn og tidspunkt gemmes allerede i auditloggen. Besluttet af mennesket | architect |
| 2026-10-22 | mockup-0002 | Resultatside efter upload (antal læst, matchet, uden match) afvist. Upload går fortsat direkte til Gennemse transport | Gennemse viser allerede antal rækker og de uafklarede øverst. En ekstra side er et ekstra klik uden ny information. Besluttet af architect, kan vendes | architect |
| 2026-10-22 | mockup-0002 | Måneden vælges fortsat på dashboardet, ikke på upload-skærmen | Dashboardet opretter kørslen for den valgte måned, og upload hører til den kørsel. Intet taler for at flytte valget. Besluttet af architect, kan vendes | architect |
| 2026-10-22 | mockup-0002 | Læsning af en fil med ugyldige rækker afvist. Hele filen afvises, til alle rækker er rettet, som i dag | Borgere uden række får ingen løn, og fejlen kan overses. En delvis fil strider mod at intet eksporteres, før alt er godkendt. Besluttet af mennesket | architect |
| 2026-10-22 | mockup-0001 | Visning af godkender og tidspunkt i listen afvist. Tooltip og auditlog bliver. Skitsen er hermed behandlet og gav ingen opgaver | Navn og tidspunkt står allerede i tooltip og auditlog. Navnet bliver ofte det samme på alle rækker, og listen er tæt. Besluttet af mennesket | architect |
| 2026-10-22 | mockup-0001 | Fortryd af enkelt godkendelse afvist. "Genåbn til rettelser" for hele kørslen er nok | En godkendelse hører til én beregning, så der er intet at rette uden en ny beregning. Fortryd ville give en ny tilstand, der skal passes sammen med eksport-spærren. Besluttet af mennesket | architect |
| 2026-10-22 | mockup-0001 | Kvittering af advarsler før godkendelse afvist. Advarsler bliver som i dag | Godkendelsen gemmer allerede hvem og hvornår, og advarslen står lige ved godkend-knappen. En kvittering ville give ét klik ekstra pr. advarsel og et nyt felt. Besluttet af mennesket | architect |
| 2026-10-22 | mockup-0001 | Blokeret borger med ret-på-stedet på godkendelsesskærmen afvist. Spærren mod manglende transport, zone og dage bliver i Undtagelser. Afgør også åbent punkt om at en blokeret borger spærrer "Godkend alle" | En kørsel kan ikke beregnes, før alle er klar, så en blokeret borger når ikke godkendelsesskærmen. Ret-på-stedet ville give to rettesteder og en ny beregning, der fjerner alle godkendelser. Besluttet af mennesket | architect |
| 2026-10-22 | mockup-0004 | R1 (skærmen ser fint ud indtil videre) afgjort: ingen handling | Reaktionen er en samlet godkendelse uden ønsker. Der er intet at bygge eller rette | architect |
| 2026-10-22 | mockup-0003 | R1 (skærmen ser fint ud indtil videre) afgjort: ingen handling | Reaktionen er en samlet godkendelse uden ønsker. Der er intet at bygge eller rette | architect |
| 2026-10-22 | mockup-0002 | R1 (skærmen ser fint ud indtil videre) afgjort: ingen handling | Reaktionen er en samlet godkendelse uden ønsker. Der er intet at bygge eller rette | architect |
| 2026-10-22 | mockup-0001 | R1 (skærmen ser fint ud indtil videre) afgjort: ingen handling | Reaktionen er en samlet godkendelse uden ønsker. Der er intet at bygge eller rette | architect |
| 2026-10-22 | — | Djangos ORM og `mssql-django` frem for `sqlalchemy` Core og `pyodbc` | Webappen er bygget i Django (admin, formularer, migreringer hviler på ORM). Planen med Django blev godkendt af mennesket. Står også under Projektspecifikke afvigelser i AGENTS.md | kickoff |
