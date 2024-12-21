from django.db import models

class FinancialTransaction(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.RESTRICT, null=False, related_name='+')
    financial_category = models.ForeignKey('financialcategories.FinancialCategory', on_delete=models.RESTRICT,
                                           null=False)
    presentation = models.ForeignKey('presentations.Presentation', on_delete=models.RESTRICT, null=True)
    selected_presentation = models.ForeignKey('selectedpresentations.SelectedPresentation', on_delete=models.RESTRICT,
                                              null=True)
    selected_exam = models.ForeignKey('selectedexams.SelectedExam', on_delete=models.RESTRICT, null=True)
    pay_category = models.ForeignKey('paycategories.PayCategory', on_delete=models.RESTRICT, null=False)
    amount = models.DecimalField(max_digits=20, decimal_places=3)
    transaction_date = models.DateTimeField(auto_now_add=True)
    pay_reference = models.CharField(max_length=30, null=True)
    recorder = models.ForeignKey('users.User', on_delete=models.RESTRICT, null=False)
    record_date = models.DateField()

    class Meta:
        db_table = 'financial_transaction'
