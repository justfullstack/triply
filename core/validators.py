# AJAX VALIDATION VIEWS
import json
import re
from django.http import JsonResponse
from django.views import View 
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        try:
            User.objects.filter(usernme=username).exists()
            return JsonResponse({'username_error': 'Username  already in  use! Please try another one! '}, status=409)
        except User.DoesNotExist:
            return JsonResponse({'username_error': ""}, status=200)


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email'] 

        try:
            validate_email(email)

            # if email valid, ensure it's not taken
            try:
                User.objects.filter(email=email).exists()
                return JsonResponse({'email_error': 'Email already in  use! Please try logging in! '}, status=409)

            except User.DoesNotExist:
                return JsonResponse({'email_error': ""}, status=200)

        except ValidationError as e:
            return JsonResponse({'email_error': str(e)}, status=400)


class SignUpPasswordOneVerificationView(View):
    def post(self, request):
        ''' returns password eror if any, else None '''
        data = json.loads(request.body)
        password = data['password1']
 

        # check length
        if len(password) < 8:
            return JsonResponse({'password_valid': False,  'message': 'Password must be at lease 8 characters long!'}, status=400)

        # spaces not allowed
        if re.search(r"\s", str(password)):
            return JsonResponse({'password_valid': False,  'message': 'Spaces not allowed!'}, status=400)

        # lower case chars
        if not re.search(r"[a-z]", str(password)):
            return JsonResponse({'password_valid': False ,  'message': 'Use at least one LOWERCASE character!'}, status=400)

        # uppercase chars
        if not re.search(r"[A-Z]", str(password)):
            return JsonResponse({'password_valid': False,  'message': 'Use at least one UPPERCASE character!'}, status=400)

        # ensure special char used
        if not re.search(r"\W", str(password)):
            return JsonResponse({'password_valid': False ,  'message': 'Use at least one SPECIAL character!'}, status=400)

        # confirm password match : done in form

        return JsonResponse({'password_valid': True}, status=200)



class SignUpPasswordTwoVerificationView(View):
    def post(self, request):
        ''' returns password eror if any, else None '''
        data = json.loads(request.body)
        password1 = data['password1']
        password2 = data['password2']

        if password1 == password2:
            return JsonResponse({'password_valid': True}, status=200)
            
        return JsonResponse({'password_valid': False ,  'message': "Password mismatch!"}, status=400)