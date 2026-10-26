from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from audit.models import log

from .forms import BorgerForm
from .models import Borger


@login_required
def borger_liste(request):
    q = request.GET.get("q", "").strip()
    borgere = Borger.objects.select_related("afdeling")
    if q:
        borgere = borgere.filter(Q(navn__icontains=q) | Q(tj_nr__icontains=q))
    if request.GET.get("vis") != "alle":
        borgere = borgere.filter(aktiv=True)
    return render(request, "register/borger_liste.html", {"borgere": borgere, "q": q})


def _gem(request, form, handling):
    ændrede = [f for f in form.changed_data if f != "cpr"]
    cpr_ændret = "cpr" in form.changed_data
    borger = form.save()
    detaljer = ", ".join(ændrede) + ("; CPR ændret" if cpr_ændret else "")
    log(request.user, handling, borger, f"{borger.navn}: {detaljer}" if detaljer else borger.navn)
    return borger


@login_required
def borger_ny(request):
    linje = None
    if request.GET.get("linje"):
        from koersel.models import Linje

        linje = get_object_or_404(Linje, pk=request.GET["linje"])
    form = BorgerForm(request.POST or None, initial={"navn": request.GET.get("navn", "")})
    if request.method == "POST" and form.is_valid():
        borger = _gem(request, form, "Oprettede medarbejder")
        if linje:
            linje.saet_borger(borger)
            linje.save()
            messages.success(request, f"{borger.navn} er oprettet og knyttet til rækken fra filen.")
            return redirect("gennemse", pk=linje.koersel_id)
        messages.success(request, f"{borger.navn} er oprettet.")
        return redirect("borger_liste")
    return render(request, "register/borger_form.html", {"form": form, "ny": True, "linje": linje})


@login_required
def borger_ret(request, pk):
    borger = get_object_or_404(Borger, pk=pk)
    form = BorgerForm(request.POST or None, instance=borger)
    if request.method == "POST" and form.is_valid():
        _gem(request, form, "Ændrede medarbejder")
        messages.success(request, f"Ændringerne for {borger.navn} er gemt.")
        return redirect("borger_liste")
    return render(request, "register/borger_form.html", {"form": form, "ny": False, "borger": borger})


@login_required
@require_POST
def vis_cpr(request, pk):
    borger = get_object_or_404(Borger, pk=pk)
    log(request.user, "Viste CPR", borger, borger.navn)
    messages.info(request, f"CPR for {borger.navn}: {borger.cpr or 'ikke registreret'}")
    return redirect("borger_ret", pk=pk)
