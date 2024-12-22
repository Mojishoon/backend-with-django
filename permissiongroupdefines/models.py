from django.db import models


class PermissionGroupDefine(models.Model):
    permission = models.ForeignKey(
        'permissions.Permission' , on_delete=models.RESTRICT, null=False)
    permission_group = models.ForeignKey('permissiongroups.PermissionGroup', on_delete=models.RESTRICT, null=False)
    recorder = models.ForeignKey('users.User', on_delete=models.RESTRICT, null=False)
    record_date = models.DateField()

    def __str__(self):
        return self.permission_group.name

    class Meta:
        db_table = 'permission_group_defines'