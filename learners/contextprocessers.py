

def get_user_name(request):
    user_name = request.user.username
    context = {'user_name': user_name}
    return context
def get_user(request):
    return request.user
