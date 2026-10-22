from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSmokeTests(TestCase):
    def test_alle_admin_lister_kan_aabnes(self):
        self.client.force_login(get_user_model().objects.create_superuser("root", password="x-test-adgangskode-1"))
        for model, model_admin in admin.site._registry.items():
            if model._meta.app_label in ("register", "stamdata", "koersel", "audit"):
                url = reverse(f"admin:{model._meta.app_label}_{model._meta.model_name}_changelist")
                self.assertEqual(self.client.get(url).status_code, 200, url)
