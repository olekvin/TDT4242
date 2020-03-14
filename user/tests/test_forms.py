from django.test import SimpleTestCase
from user.forms import SignUpForm


class TestForms(SimpleTestCase):
    def test_sign_up_form_valid_data(self):
        form = SignUpForm(
            data={
                "first_name": "Navn",
                "last_name": "Navnesen",
                "company": "NTNU",
                "email": 'navnesen@gmail.com",
                "email_confirmation": "navnesen@gmail.com",
                "phone_number": "12345678",
                "country": "Norway",
                "state": "TRONDHEIM",
                "city": "TRONDHEIM",
                "postal_code": "7030",
                "street_address": "Navnesenvei 31",
                "categories":"x"
            }
        )
        self.assertTrue(form.is_valid())

'''
"password1": "navnesen123",
                "password2": "navnesen123",
                "email": "navnesen@gmail.com",
                "email_confirmation": "navnesen@gmail.com",
                "phone_number": "12345678",
                "country": "Norway",
                "state": "TRONDHEIM",
                "city": "TRONDHEIM",
                "postal_code": "7030",
                "street_address": "Navnesenvei 31",

'''
