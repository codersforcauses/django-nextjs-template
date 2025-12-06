from django.db import models


class Feeding(models.Model):
    enclosure = models.ForeignKey('zoo.Enclosure', on_delete=models.CASCADE)
    keeper = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Feeding by {self.keeper} for {self.enclosure.name} from " + \
               f"{self.start_time} to {self.end_time}"
