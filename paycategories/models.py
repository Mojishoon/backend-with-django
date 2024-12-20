from django.db import models



class PayCategory(models.Model):
    name = models.CharField(unique=True ,max_length=100)
    recorder = models.ForeignKey('users.User', on_delete=models.RESTRICT, null=False)
    record_date = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'pay_categories'