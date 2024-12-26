from django.db import models


class RollCall(models.Model):
    presentation_session = models.ForeignKey('presentationsessions.PresentationSession' , on_delete=models.RESTRICT,
                                             null=False)
    student = models.ForeignKey('users.User', on_delete=models.RESTRICT, null=False, related_name='+')
    is_present = models.BooleanField(default=True)
    delay = models.IntegerField(null=True)
    comment = models.TextField(null=True)
    recorder = models.ForeignKey('users.User', on_delete=models.RESTRICT, null=False)
    record_date = models.DateField()

    def __str__(self):
        return self.student.first_name + " " + self.student.last_name

    class Meta:
        db_table = 'roll_calls'
        unique_together = ('student', 'presentation_session')