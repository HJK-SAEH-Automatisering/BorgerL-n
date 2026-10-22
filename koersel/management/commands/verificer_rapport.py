import hashlib

from django.core.management.base import BaseCommand, CommandError

from beregning.pdf import LAYOUT_VERSION, lav_rapport
from koersel.models import Beregningskoersel


class Command(BaseCommand):
    help = (
        "Kontrollerer, at den gemte PDF-rapport er uændret (SHA-256), og at den kan genskabes ud fra snapshotten. "
        "Den gemte PDF er altid selve beviset; en genskabt PDF er kun byte-identisk, hvis layoutet er uændret."
    )

    def add_arguments(self, parser):
        parser.add_argument("rapport_id", help="Fx 2026-10-001")

    def handle(self, *args, **opts):
        for b in Beregningskoersel.objects.select_related("koersel"):
            if b.rapport_id == opts["rapport_id"]:
                break
        else:
            raise CommandError(f"Rapport {opts['rapport_id']} findes ikke.")
        gemt = hashlib.sha256(b.pdf.read()).hexdigest()
        if gemt != b.pdf_sha256:
            raise CommandError(f"Rapport {b.rapport_id}: den gemte PDF er ændret eller beskadiget (afviger fra det registrerede SHA-256).")
        self.stdout.write(self.style.SUCCESS(f"Rapport {b.rapport_id}: den gemte PDF er uændret."))
        genskabt = hashlib.sha256(lav_rapport(b.data)).hexdigest()
        if genskabt == b.pdf_sha256:
            self.stdout.write(self.style.SUCCESS("Genskabt ud fra snapshotten: identisk."))
        elif b.data.get("rapport_layout") != LAYOUT_VERSION:
            self.stdout.write(
                f"Genskabt PDF afviger, fordi rapportens layout er ændret siden (gemt layout {b.data.get('rapport_layout', '?')}, nu {LAYOUT_VERSION}). Indholdet bygger stadig på det samme snapshot."
            )
        else:
            raise CommandError("Genskabt PDF afviger trods samme layoutversion. Undersøg snapshotten.")
