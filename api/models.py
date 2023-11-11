import uuid
from django.db import models

# Create your models here.

class Account(models.Model):
    first_name      = models.CharField(max_length= 400,blank=True)
    last_name       = models.CharField(max_length=200,blank=True)
    email_address   = models.EmailField(max_length=254, unique=True)
    phone_number    = models.CharField(max_length=15,blank=True)
    token           = models.CharField(max_length=200)
    password        = models.CharField(max_length=250)
    class Meta:
        verbose_name_plural = 'Accounts'
    def __str__(self) -> str:
        return f"{self.email_address}"

class Specimen(models.Model):
    name        = models.CharField(max_length=250)
    image       = models.ImageField(upload_to='uploads/')
    author      = models.ForeignKey(Account,on_delete=models.CASCADE)
    description = models.CharField(max_length=3000)
    longitude   = models.DecimalField(max_digits=10,decimal_places=7,blank=True,null=True)
    latitude    = models.DecimalField(max_digits=10,decimal_places=7,blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    # updated_at  = models.DateTimeField(blank=True)

    class Meta:
        verbose_name_plural = 'Specimen'

    def __str__(self) -> str:
        return f"{self.name}"

class Comment(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    specimen    = models.ForeignKey(Specimen,on_delete=models.CASCADE)
    user        = models.ForeignKey(Account,on_delete=models.CASCADE)
    comment     = models.CharField(max_length= 400)

    class Meta:
        verbose_name_plural = 'Comments'

    def __str__(self) -> str:
        return f"{self.comment}"
