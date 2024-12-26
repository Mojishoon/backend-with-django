
from rest_framework.exceptions import PermissionDenied

def pagination(objects, size, page, criteria):
    return objects.objects.filter(criteria)[(int(page)*int(size))-int(size):int(page)*int(size)]


def authorization(user, operation):
    if not user.is_superuser:
        if not user.permissions_list or not operation in user.permissions_list:
            raise PermissionDenied
    return user

