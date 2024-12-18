from django.db import models



class Building(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)
    recorder = models.ForeignKey('users.User', on_delete=models.RESTRICT, null=False)
    record_date = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'buildings'
