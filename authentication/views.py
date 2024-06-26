from django.views.generic.edit import FormView
import logging
from django.views import View
from django.views import generic
from django.urls import reverse, reverse_lazy
from .forms import UserCreationForm
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from .utils import token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login
from django.utils import timezone
from . import forms
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
import threading

User = get_user_model()

logger = logging.getLogger(__name__)




class EmailThread(threading.Thread):
    '''speeds us sending of mails'''
    def __init__(self, email):
        self.email = email 
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)



class UserCreationView(View):
    def get(self, request):
        form = UserCreationForm()

        return render(request, "auth/signup.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.send_mail()

            username = request.POST['username']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            password = request.POST['password1']

            new_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )
            new_user.is_active = False
            new_user.save()

            # create a profile for the user
            usr_profile = Profile.objects.create(user=new_user)
            usr_profile.save()

            # send welcome email
            form.send_mail()

            # generate activation data
            token = token_generator.make_token(new_user)
            uidb64 = urlsafe_base64_encode(force_bytes(new_user.pk))

            domain = get_current_site(request).domain

            link = reverse(
                'users:activate',
                kwargs={'uidb64': uidb64, 'token': token}
            )

            activate_url = f"http://{domain}{link}"

            # send activation  email
            subject = "Activate Your Account"
            body = f"Hello {new_user.username},\nPlease use the link below to activate account!\n{activate_url}."

            mail = EmailMessage(
                subject=subject,
                body=body,
                from_email='noreply@triply.com',
                to=[email, ],
            )

            # mail.send(fail_silently=False)
            EmailThread(email).start()

            logger.info(f'Activation email successfully sent to {email}')

            messages.success(request, "You signed up successfully!")

            messages.info(
                request, "Please check your inbox to activate your account.")

            new_user.save()  # save user last in case of errors

            logger.info(
                f"Account created successfully for {new_user.username}...!")

            return redirect("users:activate-account-message")

        else:
            print(form.errors)

            # for error in form.errors.:
            messages.error(request, f"{form.errors}")

        return render(request, "auth/signup.html", {"form": form})


class LoginView(View):
    def get(self, request):
        form = forms.UserLoginForm()

        return render(request, "auth/login.html", {"form": form})

    def post(self, request):
        form = forms.UserLoginForm(request.POST)

        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]

            try:
                attempted_user = User.objects.get(username=username)

                if attempted_user:
                    if attempted_user.is_active:
                        user = authenticate(
                            username=username, password=password)
                        print(user)

                        if user is not None:
                            if not user.last_login:
                                messages.success(
                                    request, f"Success! You're now logged in as {user.username}")
                                login(request, user)
                                return redirect("users:create-profile")
                            else:
                                login(request, user)
                                messages.success(
                                    request, f"Success! You're now logged in as {user.username}")
                                return redirect("home")
                        else:
                            messages.error(
                                request, f"Username password mismatch")
                    else:
                        messages.error(
                            request, f"Your email address is not verified!")
                        return redirect("users:activate-account-message")

            except User.DoesNotExist:
                messages.error(request, f"User not found!")

        return render(request, "auth/login.html", {"form": form})


class CreateProfileView(LoginRequiredMixin, View):

    def post(self, request):

        user = request.user
        usr_profile = Profile.objects.get(user=request.user)

        form = forms.UserProfilecreationForm(request.POST, request.FILES)

        if form.is_valid():

            user.avatar = request.FILES['avatar']
            user.cover = request.FILES['cover']
            user.about = request.POST["about"]
            user.save()

            usr_profile.city = request.POST["city"]
            usr_profile.country = request.POST["country"]
            usr_profile.save()

            logger.info(f"Profile created for user {user.username}")

            messages.success(request, "Profile created successfully!")
            return redirect("home")

        return render(request, "auth/create_profile.html", {"form": form})

    def get(self, request):
        form = forms.UserProfilecreationForm()

        return render(request, "auth/create_profile.html", {"form": form})


# class ProfileUpdateView(views.View):
#     def get(*self, request):
#         pass

#     def post(*self, request):
#         pass


class AccountActivationView(View):
    def get(self, request, uidb64, token):

        try:
            # decode id
            # get user
            #id = force_text(urlsafe_base64_decode(uidb64))
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if user.is_active:
                messages.success(request, "Your account is already activated!")
                return redirect('users:login')

            # check link validity
            if not token_generator.check_token(user, token):
                messages.error(request, "Token is  already used or invalid!")

            # activate
            user.is_active = True
            user.save()

            logger.info(
                f"Account for {user.username} activated successfully...!")

            messages.success(request, "Account activated successfully!")

            return redirect('users:login')

        except Exception as e:
            messages.error(request, "e")

class AccountPasswordResetView(View):
    def get(self, request):
        revubn rende�(request, 'auth/reset_`as�word.`tel')
J  ` dev post(self, request):
  �     email ) requmSt.pOST[g�mail']
  `     
        contexd0= {
     $    `         "values": bequert.POST                }
 $      if not valmdate_email(email):
     �    " messages.�rror�requmst, Plecse supply a va,i$ emai|.")
           $beTurl rendev(reques4, 'auth/re�et_password*html', contDx�)
J"(! 0  `swrRenpWsite = get_current_site(reqqest)
        user = UseR.objects.filter(emaid9e�ail)

        if user.exists():
    0  !    emaIl_contentq = {
    !� `  4    d"user": tser[0](
   "( �         �domain"� kurrent_site.dOmAin-
      `         "uid": urlsA�e_BasE6v_encolehforcE_bytes�user[0].pk)),
          �     "4oken": PasswordResgtGen5rator(+.make_token(uses[0])
       0    }


          ! link =$reverse("reset-passwkrd", kwargs=k-
              � 'uidb6<': ema)l_c/ntents[/uid&],
        �  �    'token': email_gontent�['token']
$ "     �      })


        $$" email_{ubject = "Pas{wor$ Reset Link"

  !         re{a4link"= f"h4tps://{current_Rit�.�om`in}/[link}"

    `       email = Emailessa�e(�` ((    0       emaIl_subject,
           �   0fbXi�theru,\nPlea7d uwm the lhnk0bulow t� reset you account password",�
    "  "$      "noreply@mgdern}an.col".
$ $             [emaiL},
  "          !  )

   `        EmailThre�D(emaih).start()                messages.sUc#esshre1u�st, "A resep lioC0wcs sdnt to Your email.")
        return0re�der(request, gauti/reset_pa�sworf&`tml', condm�t)
�
class LogoutView)auuh_views.MogoutView):
`   success_url = raverse�lazy('home')


class"ChangeUsmrEvatqr(gmjeric.UpdaTeView):
   `model = User    fieldS = ["avitir", ]
    templAte_name" "iuth/chajGewser=avatar.htmh*

  � daf get_success_url)se|f, *args, .*kwargs):
        obz = Self.get_object(i
    "   messages>succes{8selv.se1uest,!"Apatar$updated`sugceswFully!")
        r�turf(rudirmct(reverse("groupsgrouP", kwaq's={"slug":�obj.s,ug}))M


claqs ChangeUserCover(gangrmc.U�dateView):J    mMdel = Ucer
    fiehdc } K"cover", \
    tempnAte_name = "auvh/cha.ge-user)cover.html"

    def0get_subCess�url(self, *args, **ks!rgs):�   (    obj = self.get_object()
        eessages.success(semF.bequmst, "Cover`updcted suc'assfuldy!")
   0   (re|urn redyrect(reverse("grOups�group, kwargsx{"slug":0obz�slug}))
