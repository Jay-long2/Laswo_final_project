from django import forms

from services.models import Service

from .models import Enquiry

INPUT_CLASSES = (
    'w-full px-4 py-3 border border-gray-300 rounded-lg '
    'focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition'
)


class EnquiryForm(forms.ModelForm):
    # Bots fill in every field they find; humans never see this one.
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'tabindex': '-1', 'autocomplete': 'off'}),
        label='Leave this field empty',
    )

    class Meta:
        model = Enquiry
        fields = ['name', 'phone', 'email', 'location', 'service', 'budget_range', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }
        labels = {
            'name': 'Your name',
            'phone': 'Phone number',
            'email': 'Email address (optional)',
            'location': 'Project location',
            'service': 'What do you need?',
            'budget_range': 'Approximate budget',
            'message': 'Tell us about your project',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['service'].queryset = Service.objects.filter(is_active=True)
        self.fields['service'].empty_label = 'Select a service'
        self.fields['email'].required = False
        self.fields['location'].required = False

        placeholders = {
            'name': 'Nicholas Ngeywo',
            'phone': '07XX XXX XXX',
            'email': 'you@example.com',
            'location': 'e.g. Kitale, Trans Nzoia',
            'message': 'Plot size, number of rooms, storeys, timeline - whatever you know so far.',
        }
        for name, field in self.fields.items():
            if name == 'website':
                continue
            field.widget.attrs['class'] = INPUT_CLASSES
            if name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[name]

    def clean_website(self):
        if self.cleaned_data.get('website'):
            raise forms.ValidationError('Spam detected.')
        return ''

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('phone') and not cleaned.get('email'):
            raise forms.ValidationError(
                'Please leave either a phone number or an email so we can reply.'
            )
        return cleaned
