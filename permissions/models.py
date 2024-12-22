from django.db import models



class Permission(models.Model):
    name = models.CharField(unique=True ,max_length=100)
    parent = models.ForeignKey('self', on_delete=models.RESTRICT, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'permissions'
