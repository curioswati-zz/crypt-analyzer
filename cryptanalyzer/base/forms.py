from django import forms


class UploadFileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        for i in range(1, 5):
            self.fields['file%d' % i] = forms.FileField(label="File %d" % i)


class SelectAlgorithmForm(forms.Form):
    algo_choices = [('aes', 'AES'),
                    ('des', '3DES'),
                    ('blowfish', 'BlowFish'),
                    ('twofish', 'TwoFish'),
                    ('rc6', 'RC6')]
    choice_field = forms.MultipleChoiceField(choices=algo_choices,
                                             widget=forms.CheckboxSelectMultiple)
