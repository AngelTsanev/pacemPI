from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

'''
def user_logout(request):
    logout(request)
    return render(request, 'index.html', {})
'''
def login_user(request):
    state = "Please log in..."
    username = ''
    password = ''

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
            else:
                state = "Your account is not active!"
        else:
            state = "Your username and/or password were incorrect."

    return render_to_response('login.html',{'state':state, 'username': username})