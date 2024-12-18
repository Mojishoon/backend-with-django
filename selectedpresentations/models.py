from django.db import models


class SelectedPresentation(models.Model):
    presentation = models.ForeignKey('presentations.Presentation' , on_delete=models.RESTRICT, null=False)
    student = models.ForeignKey('users.User', on_delete=models.RESTRICT, null=False, related_name='+')
    grade = models.DecimalField(null=True, max_digits=4, decimal_places=2)
    recorder = models.ForeignKey('users.User', on_delete=models.RESTRICT, null=False)
    record_date = models.DateField()

    def __str__(self):
        return self.presentation.course.name

    class Meta:
        db_table = 'selected_presentations'