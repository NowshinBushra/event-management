from django import forms

class EventForm(forms.Form):
    title = forms.CharField(max_length=250, label="Event Title")
    description = forms.CharField(widget=forms.Textarea)
    date = forms.DateField(widget=forms.SelectDateWidget)
    time = forms.TimeField()
    location = forms.CharField(max_length=250)
    select_participants = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[])
    select_category = forms.ChoiceField(widget=forms.Select, choices=[])

    def __init__(self, *args, **kwargs):
        print(args, kwargs)
        participants = kwargs.pop("participants", [])
        categories = kwargs.pop("categories", [])
        super().__init__(*args, **kwargs)
        self.fields['select_participants'].choices=[(p.id, p.name) for p in participants]
        self.fields['select_category'].choices=[(c.id, c.name) for c in categories]


