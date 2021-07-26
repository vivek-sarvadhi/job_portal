from django.shortcuts import render, redirect
from django.views import View
from users.forms import RegisterUserForm, LoginUserForm, ProfileUserForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from users.models import CustomUser
from django.contrib.auth.views import PasswordContextMixin
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
# Create your views here.
class IndexView(View):

	def get(self, request):
		return render(request, 'users/index.html')


class RegisterView(View):

	def get(self, request):
		form = RegisterUserForm()
		return render(request, 'users/registration.html', {'form':form})


	def post(self, request):
		form = RegisterUserForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			first_name = form.cleaned_data.get('first_name')
			last_name = form.cleaned_data.get('last_name')
			user_type = form.cleaned_data.get('user_type')
			password = form.cleaned_data.get('password')
			conf_password = request.POST.get('confirm_password')

			if password == conf_password:
				saved_user = form.save(commit=False)
				saved_user.set_password(password)
				saved_user.save()
				return redirect('login')
			else:
				messages.error(request, "password or confirm password are not match")
				return render(request, 'users/registration.html', {'form':form})
			# return render(request, 'users/registration.html', {'form':form})
		messages.error(request, "email id already used")
		return render(request, 'users/registration.html', {'form':form})




class LoginView(View):

	def get(self, request):
		form = LoginUserForm
		return render(request, 'users/login.html', {'form':form})


	def post(self, request):
		form = LoginUserForm()
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = authenticate(email=email, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				if user.user_type == "jobseeker":
					return redirect('job_list')
				else:
					return redirect('apply_list')
		else:
			messages.error(request, "email or password is not correct")
			return render(request, 'users/login.html', {'form':form})
		return render(request, 'users/login.html', {'form':form})


class ProfileView(View):

	def get(self, request, pk):
		form = ProfileUserForm()
		user1 = CustomUser.objects.get(pk=pk)
		return render(request, 'users/profile.html', {'form':form, 'user1':user1})

	def post(self, request, pk):
		form = ProfileUserForm(request.POST or None, request.FILES or None, instance=request.user)
		print(form)
		if form.is_valid():
			form.save()
		return render(request, 'users/profile.html', {'form':form})


class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('login')
    template_name = 'users/change_password.html'
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)

		