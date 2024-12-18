from django.db import models


class CoursePrerequisite(models.Model):
    course = models.ForeignKey(
        'courses.Course' , on_delete=models.RESTRICT, null=False, related_name='+')
    prerequisite = models.ForeignKey('courses.Course', on_delete=models.RESTRICT, null=False)
    recorder = models.ForeignKey('users.User', on_delete=models.RESTRICT, null=False)
    record_date = models.DateField()

    def __str__(self):
        return self.course.name

    class Meta:
        db_table = 'course_prerequisites'
        unique_together = ('course', 'prerequisite')
