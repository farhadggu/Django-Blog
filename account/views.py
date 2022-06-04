#==>Library Import
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import EmailMessage
from django.contrib import messages
from django.views import View
from django.urls import resolve
import random
#==>Local Import
from .forms import RegistrationForm, VerifyCodeForm, UserLoginForm, ProfileForm
from .tokens import account_activation_token
from .models import User, OtpCode, Profile
from utils import send_otp_code


class RegistrationView(View):
    form_class = RegistrationForm
    template_name = 'register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, 'شما داخل حساب خود هستید', 'info')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone'], code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone'], code=code)
            request.session['user_registration_info'] = {
                'phone': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'username': form.cleaned_data['username'],
                'password': form.cleaned_data['password'],
            }
            messages.success(request, 'کد اعتبار سنجی برای شما فرستاده شد', 'success')
            return redirect('account:verify_code')
        messages.error(request, 'مشخصات وارد شده درست نمی باشد', 'danger')
        return render(request, self.template_name, {'form':form})


class UpdatePhoneNumberView(View):
    def post(self, request):
        url_name = resolve(request.path).url_name
        phone = request.POST.get('phone')
        code = random.randint(1000, 9999)
        request.session['user_phone'] = {
            'phone': phone,
            'url_name':url_name,
            }
        send_otp_code(phone, code)
        OtpCode.objects.create(phone_number=phone, code=code)
        messages.success(request, 'کد اعتبار سنجی برای شما فرستاده شد', 'success')
        return redirect('account:verify_code')


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'verify_code.html', {'form':form})

    def post(self, request):
        #if request.session['user_phone']:
        try:
            user_session = request.session['user_phone']
            user = User.objects.get(username=request.user.username)
            code_instance = OtpCode.objects.get(phone_number=user_session['phone'])
            form = self.form_class(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                if data['code'] == code_instance.code:
                    user.phone = str(user_session['phone'])
                    user.save()
                    code_instance.delete()
                    messages.success(request, 'شماره تلفن شما با موفقیت تغییر یافت', 'success')
                    return redirect('account:edit-profile')
                else:
                    messages.error(request, 'کد نامعتبر!', 'danger')
                    return redirect('account:code_verify')

        except:
            user_session = request.session['user_registration_info']
            code_instance = OtpCode.objects.get(phone_number=user_session['phone'])
            form = self.form_class(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                if data['code'] == code_instance.code:
                    User.objects.create_user(user_session['email'], user_session['username'],
                                            user_session['phone'], user_session['password'])

                    code_instance.delete()
                    messages.success(request, 'کاربر شما با موفقیت ایجاد شد', 'success')
                    return redirect('home:home')
                else:
                    messages.error(request, 'کد نامعتبر!', 'danger')
                    return redirect('account:code_verify')
            return redirect('account:code_verify')


class LoginView(View):
    form_class = UserLoginForm
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, 'شما داخل حساب خود هستید', 'info')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['email'], password=data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'شما با موفقیت وارد شدید', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request, 'مشخصات نامعتبر!', 'danger')
        return redirect('account:login')



class LogoutView(LoginRequiredMixin, View):
	def get(self, request):
		logout(request)
		messages.success(request, 'شما با موفقیت خارج شدید', 'success')
		return redirect('home:home')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'profile.html', {})


class EditProfileView(LoginRequiredMixin, View):
    form_class = ProfileForm
    def get(self, request):
        url_name = resolve(request.path).url_name
        print(url_name)
        form = self.form_class(instance=request.user.profile)
        return render(request, 'edit-profile.html', {'form':form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'پروفایل شما ویرایش شد', 'success')
        else:
            messages.error(request, 'خطا', 'danger')
        return redirect('account:edit-profile')


class ChangeUsernameView(LoginRequiredMixin, View):
    def post(self, request):
        username = request.POST.get('username')
        user_exist = User.objects.filter(username=username).exists()
        if user_exist:
            messages.error(request, 'همچین نام کاربری موجود می باشد', 'danger')
        else:
            user = User.objects.get(email=request.user.email)
            user.username = username
            user.save()
            messages.success(request, 'نام کاربری با موفقیت تغییر یافت', 'success')
        return redirect('account:edit-profile')


class ActivateEmailView(View):
    def post(self, request):
        user = User.objects.get(username=request.user.username)
        email = request.POST.get('email')
        current_site = get_current_site(request)
        mail_subject = 'Activate your blog account.'
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
            'email': email
        })
        to_email = email
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('Please confirm your email address to complete the registration')


class Activate(View):
    def get(self, request, uidb64, token, email):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.email = email
            user.email_activate = True
            user.save()
            # return redirect('home')
            return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')


# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         # return redirect('home')
#         return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
#     else:
#         return HttpResponse('Activation link is invalid!')


class AuthorView(View):
    def get(self, request, username):
        user = get_object_or_404(User, username=username, is_author=True)
        return render(request, 'author.html', {'user':user})