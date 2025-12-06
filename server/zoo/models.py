from django.db import models


class Habitat(models.Model):
    # id field is created automatically
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Enclosure(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    habitat = models.ForeignKey(Habitat, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
