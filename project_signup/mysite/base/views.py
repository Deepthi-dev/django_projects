from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from mysite.base.forms import SignUpForm, UserProfileInfoForm
from mysite.base.models import UserProfileInfo

# Create your views here.
def home(request):
    users_count = User.objects.count()
    return render(request, 'home.html', {
        'count': users_count
    })

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {
        'form': form,
    })

@login_required
def save_profile(request):

    registered = False
    user = request.user

    if request.method == 'POST':


        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        # if user_form.is_valid() and profile_form.is_valid():
        if profile_form.is_valid():

            profile = profile_form.save(commit=False)

            profile.user = request.user

            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True

        else:
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        try:
            profile_form = UserProfileInfo.objects.get(user=request.user)
            registered = True

        except:
            profile_form = UserProfileInfoForm()


    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'save_profile.html',
                          {'profile_form': profile_form,
                           'user': user,
                           'registered':registered})

    # return render(request, 'save_profile.html')
