from django import forms
from .models import NFTProject


class ProjectForm(forms.ModelForm):
    class Meta:
        model = NFTProject
        fields = ("name", "contract_address", "contract_abi", "number_of_nfts")


class ConfirmForm(forms.Form):
    hidden = forms.HiddenInput()
