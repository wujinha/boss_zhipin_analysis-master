from django.http import JsonResponse


def success(data='success', message='成功'):
    return JsonResponse({'code': 0, 'message': message, 'data': data})


def error(message='失败', status=200, data='error'):
    res = JsonResponse({'code': 1, 'message': message, 'data': data})
    res.status_code = status
    return res


def redirect(link='', message='成功'):
    return JsonResponse({'code': 2, 'message': message, 'data': link})
