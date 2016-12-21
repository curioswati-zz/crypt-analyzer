from django.db import models


# Create your models here.
class EncryptedFile(models.Model):
    '''
    model to save uploaded files.
    '''
    name = models.CharField(max_length=30)
    file_data = models.FileField(upload_to='files')

    def __str__(self):
        return self.name.split('/')[-1]
