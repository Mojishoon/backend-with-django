from django.db import models


class Presentation(models.Model):
    course = models.ForeignKey(
        'courses.Course' , on_delete=models.RESTRICT, null=False)
    teacher = models.ForeignKey('users.User', on_delete=models.RESTRICT, null=False, related_name='+')
    is_private = models.BooleanField(default=False)
    session_count = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    recorder = models.ForeignKey('users.User', on_delete=models.RESTRICT, null=False)
    record_date = models.DateField()

    def __str__(self):
        return self.course.name

    class Meta:
        db_table = 'presentations'
