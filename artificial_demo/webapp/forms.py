from django import forms
from django.forms import FloatField
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import BankModel,Predictions

class UploadFileForm(forms.Form):
    file = forms.FileField()


class CustomerForm(forms.ModelForm):
    
    class Meta:

        model = Predictions

        #fields = '__all__'
        fields = ['age','job', 'marital', 'education', 'default', 'balance', 'housing','loan', 'contact', 'day', 'month', 'duration','campaign','pdays','previous','poutcome']
        # labels = {
        #     'term': _('Loan term'),
        # }
        # help_texts = {
        #     'term': _('Choose the term of your loan'),
        # }
        # error_messages = {
        #     'loan_amnt': {
        #         'max_length': _("Maximum loan amount allowed is 35000."),
        #     },
        # }

