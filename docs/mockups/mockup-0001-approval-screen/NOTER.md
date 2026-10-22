---
nummer: mockup-0001
titel: Godkendelsesskærmen
status: behandlet
oprettet: 2026-10-22
---

# mockup-0001 — Godkendelsesskærmen

## Hvad blev vist
1. Godkendelsesskærmen for september 2026 med otte fiktive borgere: trin-bjælke, fem totaler (borgere, løn før skat, løn efter skat, træk 991, udbetaling 991), knapper og liste pr. borger.
2. Pr. borger: navn, Tj.nr., afdeling, timer, transporttype, zoner, beløb, status og knap til at godkende. "Se beregningsgrundlag" folder trin for trin ud, hvordan beløbet er nået.
3. Advarsler (dobbeltansættelse, afdeling mangler) som gule bånd, der ikke blokerer.
4. En borger uden zone er blokeret med rødt bånd. Her kan transport og zone rettes, og beregningen køres igen.
5. Filtre: Alle, Afventer, Advarsler, Kan ikke godkendes.
6. "Godkend alle" godkender alle der kan, og melder hvor mange der blev sprunget over.
7. Eksport er låst, til alle er godkendt. Derefter vises "Godkendt" og "Genåbn til rettelser".
8. "Beregn igen" med advarsel om at godkendelser bortfalder, og en historik over tidligere rapporter.

## Hvad slutbrugeren reagerede på
R1. Hele skærmen blev vist for slutbrugeren, som mente, at den ser fint ud indtil videre. Der kommer rettelser løbende. Intet i skitsen er ændret som følge af det.

## Hvad blev valgt fra
intet endnu.

## Hvilke data skærmen forudsætter
Det der findes i datamodellen i dag (læst fra modelfilerne, ingen værdier):
- Kørsel: måned og status. Beregningskørsel: nummer, tidspunkt, bruger, rapport-id.
- Resultat pr. borger: navn, Tj.nr., afdeling, timer, løn før og efter skat, træk 991, udbetaling 991, godkendt, godkendt af og hvornår.
- Beregningsgrundlag pr. borger som liste af trin (titel, formel, indsat, resultat, evt. note) og en liste af advarsler.

Det skærmen viser, men som ikke findes som egen struktur i dag:
- Advarsler skal kunne **blokere** godkendelse (zone mangler), ikke kun advare. Et skel mellem blokerende og ikke-blokerende advarsler findes ikke i modellen.
- Retning af en blokeret borger direkte på godkendelsesskærmen (transport og zone) findes ikke i dag. Rettelser sker i undtagelser.
- Afdeling mangler, dobbeltansættelse som automatisk kontrol.
- Filtrering på status og advarsler.

## Gæt
- Satserne i skitsen (timesats, skat, zonepriser) er opdigtet. Kun formen er fra reglerne: egenbetaling højst 30 % af løn efter skat, 2 zoner som egenbetalingsgrænse.
- Antal dage bruges for alle transporttyper; ved individuel beregning kaldes de fremmødedage. Valgt frem for at vise en separat dagsberegning for standard.
- Taxa giver træk i lønnen svarende til egenbetaling. Kører selv giver udbetaling = zonepris − egenbetaling. Valgt ud fra reglerne i løsningsforslaget; ikke bekræftet af fagperson.
- Blokeret borger kan rettes på selve skærmen. Valgt frem for at sende brugeren tilbage til undtagelser, for at vise at spærren kan løses hurtigt.
- Rettelse kører en ny beregning og fjerner alle godkendelser. Valgt fordi det er sådan "Beregn igen" virker i dag.
- "Genåbn til rettelser" fjerner alle godkendelser. Uklart hvad den gør i dag.
- Dobbeltansættelse og manglende afdeling vises som advarsler, der ikke blokerer.

## Åbent
- Skal en advarsel kunne kvitteres ("set og accepteret") før godkendelse?
- Skal godkendelse kunne fortrydes pr. borger?
- Er det rigtigt, at en blokeret borger spærrer "Godkend alle" for de andre, eller skal de andre gå igennem?
- Skal slutbrugeren kunne se hvem der godkendte hvem, direkte i listen?

## Afledte numre
intet — alle åbne punkter og forslag er afvist; se beslutningsloggen.
