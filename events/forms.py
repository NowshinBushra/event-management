from django import forms
from events.models import Event, Category 
# from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model


User = get_user_model()


class StyledFormMixin:
    """ Mixing to apply style to form field"""

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()

    default_classes = "border-2 bg-white border-gray-600 w-full p-3 my-2 rounded-lg shadow-sm focus:outline-none focus:border-slate-800 focus:ring-slate-800"

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
                field.widget.attrs.update({
                    "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-slate-800 focus:ring-yellow-600"
                })
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({
                    "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-slate-800 focus:ring-yellow-600"
                })
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} space-y-2 text-green",
                    'placeholder':  f"Select {field.label}",
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                     'class': "space-y-2"
                })
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })


class EventModelForm(StyledFormMixin, forms.ModelForm):

    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='User'), 
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'location', 'category', 'participants', 'asset']
        
        widgets = {
            'date' : forms.SelectDateWidget, 
            'time': forms.TimeInput(attrs={'type': 'time'}), 
            'category': forms.Select
            }
        


class CategoryModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
