from django import forms


class UploadFileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        for i in range(1, 5):
            self.fields['file%d' % i] = forms.FileField(label="File %d" % i)


class SelectAlgorithmForm(forms.Form):
    aes = forms.BooleanField(label="AES", required=False)
    des = forms.BooleanField(label="3DES", required=False)
    blowfish = forms.BooleanField(label="BlowFish", required=False)
    twofish = forms.BooleanField(label="TwoFish", required=False)
    rc6 = forms.BooleanField(label="RC6", required=False)

#    SAMPLE_CHOICES = [('aes', 'AES'),
#                      ('des', '3DES'),
#                      ('blowfish', 'BlowFish'),
#                      ('twofish', 'TwoFish'),
#                      ('rc6', 'RC6')]
#    choice_field = forms.MultipleChoiceField(choices=SAMPLE_CHOICES,
#                                             widget=forms.CheckboxSelectMultiple)
