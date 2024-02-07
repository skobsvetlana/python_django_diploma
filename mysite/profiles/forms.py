from django import forms

from profiles.models import Profile

class ProfileUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    phone = forms.CharField(max_length=15,
                            required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['avatar',]

