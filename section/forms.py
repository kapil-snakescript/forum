from django import forms
from .models import Section


class AddSectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk') 
        # remove this b4 calling super otherwise it will complian
        super(AddSectionForm, self).__init__(*args, **kwargs)


    topic = forms.CharField(max_length=50)
    title = forms.CharField(max_length=50)
    description = forms.CharField(max_length=2000)

    def clean(self):
        
        title_text = self.cleaned_data.get('title')
        # print(self.pk)
        if self.pk:
            section =  Section.objects.filter(id=self.pk).first()
            if not section.title == title_text:
                if Section.objects.filter(title=title_text).exists():
                    raise forms.ValidationError("This Section name already exists please try another")
        elif Section.objects.filter(title=title_text).exists():
            raise forms.ValidationError("This Section name already exists please try another")

        
        


