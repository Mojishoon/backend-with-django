from django.db import models



class ExamSchedule(models.Model):
    exam = models.ForeignKey('exams.Exam', on_delete=models.RESTRICT, null=False)
    start_date = models.DateField()
    recorder = models.ForeignKey('users.User', on_delete=models.RESTRICT, null=False)
    record_date = models.DateField()

    def __str__(self):
        return self.exam.course.name

    class Meta:
        db_table = 'exam_schedules'
