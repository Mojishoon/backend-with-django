from django.db import models



class Lesson(models.Model):
    name = models.CharField(unique=True ,max_length=100)
    lesson_group = models.ForeignKey('lessongroups.LessonGroup', on_delete=models.RESTRICT, null=False)
    recorder = models.ForeignKey('users.User', on_delete=models.RESTRICT, null=False)
    record_date = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'lessons'
