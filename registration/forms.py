from django import forms
from .models import User

class EditProfileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk') 
        # remove this b4 calling super otherwise it will complian
        super(EditProfileForm, self).__init__(*args, **kwargs)

    fullname = forms.CharField(max_length=30)
    username = forms.CharField(max_length=20)


    def clean(self):
        
        username_text = self.cleaned_data.get('username')
        user =  User.objects.filter(id=self.pk).first()
        if not user.username == username_text:
            if User.objects.filter(username=username_text).exists():
                raise forms.ValidationError("This Nickname already exists please try another")


