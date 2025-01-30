from django import forms
from events.models import Event, Participant


# class EventForm(forms.Form):
#     name = forms.CharField(max_length=250, label="Event Title")
#     description = forms.CharField(widget=forms.Textarea)
#     date = forms.DateField(widget=forms.SelectDateWidget)
#     time = forms.TimeField()
#     location = forms.CharField(max_length=250)
#     select_participants = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[])
#     select_category = forms.ChoiceField(widget=forms.Select, choices=[])

#     def __init__(self, *args, **kwargs):
#         print(args, kwargs)
#         participants = kwargs.pop("participants", [])
#         categories = kwargs.pop("categories", [])
#         super().__init__(*args, **kwargs)
#         self.fields['select_participants'].choices=[(p.id, p.name) for p in participants]
#         self.fields['select_category'].choices=[(c.id, c.name) for c in categories]


class StyledFormMixin:
    """ Mixing to apply style to form field"""

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()

    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder':  f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                # print("Inside Date")
                field.widget.attrs.update({
                    "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
                })
            elif isinstance(field.widget, forms.TimeInput):
                # print("Inside Date")
                field.widget.attrs.update({
                    "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
                })
            elif isinstance(field.widget, forms.Select):
                # print("Inside checkbox")
                field.widget.attrs.update({
                    'class': f"{self.default_classes} space-y-2 text-green",
                    'placeholder':  f"Select {field.label.lower()}",
                })
            else:
                # print("Inside else")
                field.widget.attrs.update({
                    'class': self.default_classes
                })


class EventModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        # fields = '__aLL__'
        fields = ['title', 'description', 'date', 'time', 'location', 'category']
        
        widgets = {'date' : forms.SelectDateWidget, 'category': forms.Select}