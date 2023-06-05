from django.db import models

# Create your models here.
class ConfigCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    
    def __str__(self):
        return str(self.name)
    
class ConfigChoice(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to="choice/", blank=True)
    is_active = models.BooleanField()
    category = models.ForeignKey(ConfigCategory, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.name)