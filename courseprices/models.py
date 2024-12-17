from django.db import models



class CoursePrice(models.Model):
    public_price = models.DecimalField(decimal_places=3, max_digits=10)
    private_price = models.DecimalField(decimal_places=3, max_digits=10)
    date = models.DateField()
    duration = models.FloatField()
    course = models.ForeignKey('courses.Course', on_delete=models.RESTRICT, null=False)
    recorder = models.ForeignKey('users.User', on_delete=models.RESTRICT, null=False)
    record_date = models.DateField()

    def __str__(self):
        return self.course.name

    class Meta:
        db_table = 'course_prices'
