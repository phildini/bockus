import dropbox
from django import forms


class ImportForm(forms.Form):

    def __init__(self, *args, **kwargs):
        token = kwargs.pop('token')
        client = kwargs.pop('client')
        super(ImportForm, self).__init__(*args, **kwargs)
        choices = [('select_all_option', 'Select All')]
        metadata = client.metadata('/')
        directories = [(item.get('path'), item.get('path')) for item in metadata.get('contents') if item.get('is_dir')]
        choices += directories

        self.fields['folders'] = forms.MultipleChoiceField(
            required=True,
            choices=choices,
            widget=forms.CheckboxSelectMultiple(),
        )
