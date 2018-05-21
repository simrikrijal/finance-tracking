from django.test import TestCase

from .. import forms


class AccountCreateFormTests(TestCase):
    def test_available_fields(self):
        form = forms.AccountCreateForm()
        fields = ['name', 'initial_balance', 'active', 'show_on_dashboard']
        self.assertEqual(len(form.fields), len(fields))
        for field in fields:
            self.assertIn(field, form.fields)

    def test_form_saves_initial_balance(self):
        form = forms.AccountCreateForm({
            'name': 'foo', 'initial_balance': 100, 'active': True, 'show_on_dashboard': False})
        account = form.save()
        self.assertEqual(account.balance, 100)
        self.assertEqual(account.name, 'foo')
        self.assertTrue(account.active)
        self.assertFalse(account.show_on_dashboard)
