from django.db import models



class Holiday(models.Model):
    holiday_date = models.DateField(unique=True)
    recorder = models.ForeignKey('users.User', on_delete=models.RESTRICT, null=False)
    record_date = models.DateField()

    def __str__(self):
        return self.holiday_date

    class Meta:
        db_table = 'holidays'
