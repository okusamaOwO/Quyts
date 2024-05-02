from django import forms

class RoundedTextarea(forms.Textarea):
    def __init__(self, attrs=None):
        default_attrs = {'class': 'rounded-textarea'}
        if attrs:
            attrs.update(default_attrs)
        else:
            attrs = default_attrs
        super().__init__(attrs)