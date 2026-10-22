from django import forms
from django.core.exceptions import ValidationError

from stamdata.models import ZonePris

from .models import Borger, normaliser_cpr


class BorgerForm(forms.ModelForm):
    cpr = forms.CharField(
        label="CPR-nummer",
        required=False,
        max_length=13,
        widget=forms.TextInput(attrs={"autocomplete": "off", "placeholder": "ddmmåå-xxxx"}),
    )

    class Meta:
        model = Borger
        fields = ["navn", "tj_nr", "cpr", "adresse", "afdeling", "arbejdssted", "afstand_km", "transport", "zoner", "sats", "traek_procent", "aktiv"]
        widgets = {"zoner": forms.Select()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        zoner = sorted(ZonePris.gaeldende())
        self.fields["zoner"] = forms.TypedChoiceField(
            label="Standard-zoner",
            required=False,
            coerce=int,
            empty_value=None,
            choices=[("", "-")] + [(z, str(z)) for z in zoner],
        )
        self.initial["cpr"] = ""
        if self.instance.pk and self.instance.cpr:
            self.fields["cpr"].help_text = f"Nuværende: {self.instance.cpr_maskeret}. Udfyld kun for at ændre."
        self.fields["transport"].choices = [("", "Vælg")] + list(Borger._meta.get_field("transport").choices)

    def clean_cpr(self):
        try:
            return normaliser_cpr(self.cleaned_data.get("cpr", ""))
        except ValidationError as e:
            raise forms.ValidationError(e.messages)

    def clean_tj_nr(self):
        tj = (self.cleaned_data.get("tj_nr") or "").strip()
        return tj or None

    def save(self, commit=True):
        borger = super().save(commit=False)
        if not self.cleaned_data.get("cpr") and self.instance.pk:
            borger.cpr = Borger.objects.get(pk=self.instance.pk).cpr
        if commit:
            borger.save()
        return borger
