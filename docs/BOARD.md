# BOARD

Tilstandsrapport. Svarer på: **hvad er åbent, og hvad venter på mig.** Skal kunne skimmes på ti sekunder.

**Skrives af `architect`**, som er den eneste rolle der opretter opgaver, sætter statusser og triagerer rapporter. Opdateres før tråden lukkes. Ingen agent skriver her.

`status` skriver den ikke — den læser den, holder den op mod filerne, og siger til hvis den er skredet. **Er BOARD uenig med en fil, er filen rigtig.**

**Ingen prosa i tabellerne.** Ingen commit-hashes, filstier, datoer eller begrundelser. Begrundelser hører i `docs/decisions/log.md`.

## Rapporter klar til behandling

| Nr. | Rolle | Uafhentede punkter |
|---|---|---|

<En rapport står her indtil hvert af dens fund er blevet en opgave eller er
afvist i beslutningsloggen. Det er det eneste sted et fund kan forsvinde —
en rapport der har stået her i dagevis, er et fund på vej til at blive glemt.>

## Opgaver

| Nr. | Titel | Status | Kilde |
|---|---|---|---|

<`Status` er `planlagt`, `i-gang` eller `afsluttet`. `Kilde` er `interview`
eller nummeret på den rapport opgaven kom af.>

## Kommende

| Emne |
|---|
| Indfør versionsnummer, start på 0.1.0, før første udrulning |

<Den grove liste: hvad architect kan se der skal laves. **Ingen numre.**
Et emne får først et nummer når interviewet har gjort det udførbart —
ellers fyldes `docs/tasks/` med halve idéer.>

## Afsluttet

| Nr. | Titel | Udfald |
|---|---|---|
| task-0001 | Tydeligere kørselsskærme: sidst uploadet og første manglende række | afvist |
| task-0002 | Tydeligere kørselsskærme: sidst uploadet og første manglende række | bygget |
| task-0003 | Indlæs .env automatisk i indstillingerne | bygget |
| task-0004 | Trin som knapper i venstre side og antal dage fra Punchly-filen | bygget |
| task-0005 | Simplificér Godkend-skærmen | bygget |
| task-0006 | Beregningsgrundlag som knap og egen side på Godkend-skærmen | bygget |
| task-0007 | Skift ordet borger til medarbejder, og navnet BorgerLøn til MedarbejderLøn | bygget |
| task-0008 | Afklar uden valg giver en besked i stedet for en serverfejl | bygget |
| task-0009 | Placér knappen Beregningsgrundlag ved siden af Godkend | bygget |
| task-0010 | Fjern knappen Tilbage til undtagelser på Godkend-skærmen | bygget |
| task-0011 | Få browseren til at hente nyt stylesheet og ny skærmkode, når de ændres | bygget |
| task-0012 | Rækkerne på Godkend-skærmen skifter ikke plads, når nogle er godkendt | bygget |

<`Udfald` er `bygget` eller `afvist`. Flyt hertil når architect har vurderet
opgaven — ikke når udrulningen er sket; udrulning er ikke en status.
Slet ikke herfra; historikken er billig.>
