from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from InitApp.models import User
import bcrypt

def index(request):
    if 'user' not in request.session:
        messages.error(request, 'You are NOT logged')
        return redirect("/SignUp/")
    context = {
    }
    return redirect("/logIn/")

def register(request):
    if request.method == "GET":
        context = {}
        if 'user' in request.session:
            messages.warning(request, 'You re logged')
            return render(request, "logIn.html", context)
        return render(request, "index.html", context)

    if request.method == "POST":
        print("Post register ",request.POST)
        errors = User.objects.validations_signup(request.POST)
        print(errors)
        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request,v)
            return redirect('/')
        else:
            messages.success(request,"You Signed up successfully")

            encrypted_pwd = bcrypt.hashpw(request.POST['pwd'].encode(), bcrypt.gensalt()).decode()
            print(f"The password '{request.POST['pwd']}' using bcrypt, the results is {encrypted_pwd}")

            user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'].lower(),
                password = encrypted_pwd,
                birthday = request.POST['bday']
            )

            session_user = {
                'id' : user.id,
                'name' : user.first_name + ' ' + user.last_name,
                'email' : user.email
            }
            print(session_user)
            request.session['user'] = session_user

            context = {}
            return render(request, "logIn.html", context) #Change to success

def access(request):
    if request.method == "GET":
        context = {}
        if 'user' in request.session:
            messages.warning(request, 'You re logged')
            return render(request, "logIn.html", context)
        return render(request, "index.html", context)

    if request.method == "POST":
        print("Post register ",request.POST)
        
        errors = User.objects.validations_login(request.POST)
        print(errors)
        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request,v)
            return redirect('/')
        else:
            user = User.objects.filter(email=request.POST['email'].lower())
            if user:
                logged_user = user[0]
                encrypted_pwd = bcrypt.hashpw(request.POST['pwd'].encode(), bcrypt.gensalt()).decode()
                print(f"The password '{request.POST['pwd']}' using bcrypt, the results is {encrypted_pwd}")
                if bcrypt.checkpw(request.POST['pwd'].encode(), logged_user.password.encode()):

                    session_user = {
                    'id' : logged_user.id,
                    'name' : logged_user.first_name + ' ' + logged_user.last_name,
                    'email' : logged_user.email
                    }

                    print(session_user)
                    request.session['user'] = session_user

                    context = {}
                    messages.success(request,"You logged In successfully")
                    return render(request, "logIn.html", context)
                else:
                    messages.error(request,"Wrong Password. Retry!")
                    return redirect("/")
            else:
                messages.error(request,"The email has not own users")    
                return redirect("/")

def logout(request):
    if 'user' in request.session:
        del request.session['user']
    return redirect("/")    

#con sesion iniciada, no ir a iniciar sesion