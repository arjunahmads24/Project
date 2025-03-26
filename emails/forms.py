from django import forms
from .models import Email

class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['email']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = ''
        self.fields['email'].widget.attrs.update({'placeholder': 'Your Email'})
    def clean(self):
        data = self.cleaned_data
        email = data.get('email')
        qs = Email.objects.filter(email__iexact=email)
        if qs.exists():
            self.add_error('email', 'Email telah terdaftar. Silahkan gunakan email yang lain.')
        return data
