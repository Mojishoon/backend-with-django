
def pagination(objects, size, page, criteria):
    return objects.objects.filter(criteria)[(int(page)*int(size))-int(size):int(page)*int(size)]

