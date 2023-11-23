import xrpl
from django.db import models

# Create your models here.

class ACCOUNT(models.Model):
    wallet_address = models.CharField(max_length=100,null=False)
    private_key = models.CharField(max_length=100,null=False)
    public_key = models.CharField(max_length=100,null=False)
    balance = models.CharField(max_length=100,null=False)
    seed = models.CharField(max_length=100,null=True,default=None)
    def __str__(self) -> str:
        return str(self.wallet_address)