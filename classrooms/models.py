from django.db import models



class Classroom(models.Model):
    name = models.CharField(unique=True ,max_length=100)
    floor = models.IntegerField()
    capacity = models.IntegerField()
    building = models.ForeignKey('buildings.Building',on_delete=models.RESTRICT, null=False)
    lesson_group = models.ForeignKey('lessongroups.LessonGroup', on_delete=models.RESTRICT, null=True)
    recorder = models.ForeignKey('users.User', on_delete=models.RESTRICT, null=False)
    record_date = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'classrooms'
