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

    def get_lower_percentage(self):
        return self.lower_percentage
    
    def get_upper_percentage(self):
        return self.upper_percentage

    def get_min_value(self):
        return self.min_value


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

    def get_id_comission(self):
        return self.comission.pk


class Month_Comissions(models.Model):

    id_seller = models.ForeignKey(Sellers, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.IntegerField()
    comission = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Comissão Mensal Vendedor"
        verbose_name_plural = "Comissões Mensal Vendedor"

    def __str__(self):
        return str(self.pk)
