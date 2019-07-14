from django.db import models


class Comissions(models.Model):

    lower_percentage = models.FloatField()
    min_value = models.FloatField()
    upper_percentage = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Comissão"
        verbose_name_plural = "Comissões"

    def __str__(self):
        return str(self.pk)


class Sellers(models.Model):

    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    age = models.IntegerField()
    email = models.EmailField(max_length=254)
    cpf = models.CharField(max_length=50)
    comission = models.ForeignKey(Comissions, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Vendedor"
        verbose_name_plural = "Vendedores"

    def __str__(self):
        return self.name
