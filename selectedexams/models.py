from django.db import models


class SelectedExam(models.Model):
    exam_schedule = models.ForeignKey('examschedules.ExamSchedule' , on_delete=models.RESTRICT, null=False)
    student = models.ForeignKey('users.User', on_delete=models.RESTRICT, null=False, related_name='+')
    is_participated = models.BooleanField(default=True)
    grade = models.DecimalField(null=True, max_digits=4, decimal_places=2)
    recorder = models.ForeignKey('users.User', on_delete=models.RESTRICT, null=False)
    record_date = models.DateField()

    def __str__(self):
        return self.student.name

    class Meta:
        db_table = 'selected_exams'