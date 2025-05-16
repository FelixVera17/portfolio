from django.db import models

class Ruc(models.Model):
    documento = models.CharField(max_length=50)
    nombre = models.CharField(max_length=255)
    codigo =  models.CharField(max_length=20)
    clave = models.CharField(max_length=20)
    
    def __str__(self):
        return f'{self.codigo} - {self.nombre}'
    
    
    
class CargaRuc(models.Model):
    name_arc = models.CharField(max_length=255)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    registros = models.PositiveIntegerField()
    
    def __str__(self):
        return f'{self.name_arc} - {self.fecha_carga.strftime("%Y-%m-%d %H:%M:%S")}'    