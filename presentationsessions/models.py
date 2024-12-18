from django.db import models


class PresentationSession(models.Model):
    presentation = models.ForeignKey('presentations.Presentation' , on_delete=models.RESTRICT, null=False)
    classroom = models.ForeignKey('classrooms.Classroom', on_delete=models.RESTRICT, null=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_cancelled = models.BooleanField(default=False)
    is_extra = models.BooleanField(default=False)
    recorder = models.ForeignKey('users.User', on_delete=models.RESTRICT, null=False)
    record_date = models.DateField()

    def __str__(self):
        return self.presentation.course.name

    class Meta:
        db_table = 'presentation_sessions'