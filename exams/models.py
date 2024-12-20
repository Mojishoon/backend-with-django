from django.db import models



class Exam(models.Model):
    price = models.DecimalField(decimal_places=3, max_digits=10)
    course = models.ForeignKey('courses.Course', on_delete=models.RESTRICT, null=False)
    recorder = models.ForeignKey('users.User', on_delete=models.RESTRICT, null=False)
    record_date = models.DateField()

    def __str__(self):
        return self.course.name

    class Meta:
        db_table = 'exams'
