# Beslutningslog

Append-only. Nyeste øverst. Én linje pr. beslutning.

**Ejes af `architect`.** Dens tråd er den eneste samtale i modellen, og loggen er det eneste spor af den der overlever tråden. Hver beslutning truffet i en `architect`-tråd skrives ind, med begrundelse, før tråden lukkes.

Her hører også **afvisninger**: et fund der ikke bliver en opgave, skal have sin begrundelse her. Ellers er det et fund der forsvandt.

`Nr.` er nummeret beslutningen hører til — `task-0042`, `test-0003` — eller `—` hvis den gælder projektet som helhed.

| Dato | Nr. | Beslutning | Begrundelse | Rolle |
|---|---|---|---|---|
| 2026-10-22 | — | Djangos ORM og `mssql-django` frem for `sqlalchemy` Core og `pyodbc` | Webappen er bygget i Django (admin, formularer, migreringer hviler på ORM). Planen med Django blev godkendt af mennesket. Står også under Projektspecifikke afvigelser i AGENTS.md | kickoff |
