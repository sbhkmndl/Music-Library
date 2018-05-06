from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse,Http404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import login, get_user_model, logout
from django.views.generic.edit import CreateView, FormView
from django.contrib import messages

from .form import UserLoginForm, UserCreationForm,PasswordForgetForm,ResetPasswordForm,ForgetPasswordForm
from .models import PasswordForget

# Create your views here
User = get_user_model()


class LoginCheckMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/edit/user')
        return super(LoginCheckMixin, self).dispatch(request, *args, **kwargs)


# Login View
class UserLoginView(LoginCheckMixin, FormView):
    model = User
    form_class = UserLoginForm
    template_name = 'profile/user_login.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        context = self.get_context_data()
        if form.is_valid():
            login(request, form.cleaned_data.get('user'))
            return HttpResponseRedirect('/edit/user')
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(UserLoginView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['title'] = 'Login'
        return context


# Create View
class UserCreateView(LoginCheckMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'profile/user_signup.html'
    # success_url = '/profile/login/'

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Register'
        return context

    def get_success_url(self):
        messages.success(self.request, 'Successfully Created')
        return reverse('user_login')


# Logout view
class UserLogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/profile/login/')


# forget Password
class UserForgetPasswordView(LoginCheckMixin, CreateView):
    form_class = PasswordForgetForm
    template_name = 'profile/forget_password.html'

    def get_context_data(self, **kwargs):
        context = super(UserForgetPasswordView, self).get_context_data(**kwargs)
        context['title'] = 'Forget Password'
        return context

    def get_success_url(self):
        messages.success(self.request, 'Reset link send to your email')
        return reverse('user_login')


# Reset password
class ResetPasswordView(LoginCheckMixin, FormView):
    form_class = ResetPasswordForm
    template_name = 'profile/reset_password.html'

    def dispatch(self, request, *args, **kwargs):
        # get key from url
        key = kwargs.get('key')
        # get related table data from database
        key_exist = PasswordForget.objects.filter(Q(code=key), Q(active=True))
        if not key_exist.exists():
            raise Http404
        return super(ResetPasswordView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        context = self.get_context_data()
        if form.is_valid():
            key = kwargs.get('key')
            password = form.cleaned_data.get('password')
            reset_data = PasswordForget.objects.filter(Q(code__iexact=key), Q(active=True)).first()
            user = reset_data.user
            # set new user password
            user.set_password(password)
            # save password
            user.save()
            # deactivate key from database
            reset_data.active = False
            reset_data.save()
            messages.success(self.request, 'Password SuccessFully Changed')
            return HttpResponseRedirect('/profile/login')
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ResetPasswordView, self).get_context_data(**kwargs)
        context['title'] = 'Reset Password'
        return context


# Login required Mixin
class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin,self).dispatch(request, *args, **kwargs)


# Change password
class ChangePasswordView(LoginRequiredMixin, FormView):
    form_class = ForgetPasswordForm
    template_name = 'profile/change_password.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        context = self.get_context_data()
        if form.is_valid():
            prev_password = form.cleaned_data.get('current_password')
            if not request.user.check_password(prev_password):
                context['invalid_password'] = "Wrong Password"
                return self.render_to_response(context)
            new_password = form.cleaned_data.get('new_password')
            request.user.set_password(new_password)
            request.user.save()
            messages.success(self.request, 'Password SuccessFully Changed')
            return HttpResponseRedirect('/profile/login')
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ChangePasswordView, self).get_context_data(**kwargs)
        context['title'] = 'Change Password'
        return context
