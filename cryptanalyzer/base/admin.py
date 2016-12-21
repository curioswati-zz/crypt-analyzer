from django.contrib import admin
from . import models


# Register your models here.
class EncryptedFileAdmin(admin.ModelAdmin):
    list_per_page = 10


admin.site.register(models.EncryptedFile, EncryptedFileAdmin)
