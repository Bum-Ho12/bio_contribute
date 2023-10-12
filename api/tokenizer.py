"""
model that deals with generation of tokens
follows the rest_framework.authtoken model but bypasses the settings.USER_MODEL
requirements rather fetches the Account model from models.py of the app -> "api"
"""
import binascii
import os
from django.db  import models
from .models import Account
from django.utils.translation import gettext_lazy as _

class AuthToken(models.Model):
    key     = models.CharField(_("Key"),max_length=40,primary_key=True)
    user    = models.OneToOneField(
        Account,related_name='auth_token',
        on_delete=models.CASCADE,verbose_name=_("User")
    )
    created_at = models.DateTimeField(_("CreatedAt"),auto_now_add=True)

    def save(self,*args,**kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args,**kwargs)
    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()
    def __str__(self):
        return self.key