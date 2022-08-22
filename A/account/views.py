from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .forms import UserRefistrationForm, UserLoginForm, ResetPasswordForm, EditUserForm
from home.models import Post
from .models import Relation, Profile


class UserRegisterView(View):
    form_class = UserRefistrationForm
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            messages.success(request, 'you registered successfully', 'success')
            return redirect('home:home')
        return render(request, self.template_name, {'form':form})


class UserloginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'logged in successfully', 'success')
                if self.next:
                    return redirect(self.next)
                else:
                    return redirect('home:home')
            else:
                messages.error(request, 'username or password is wrong', 'warning')
        return render(request, self.template_name, {'form': form})

class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'logged out successfully', 'success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        is_following = False
        user = get_object_or_404(User, pk=user_id)
        bio = user.profile
        posts = user.posts.all()  # Post.objects.filter(user=user)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        follower_count = Relation.objects.filter(to_user=user).count()
        following_count = Relation.objects.filter(from_user=user).count()
        if relation.exists():
            is_following = True
        return render(request, 'account/profile.html', {'user': user,
                                                        'posts': posts,
                                                        'is_following': is_following,
                                                        'bio': bio,
                                                        'followers': follower_count,
                                                        'following': following_count})


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'


class UserPasswordResetView2(LoginRequiredMixin, View):
    form_class = ResetPasswordForm
    template_name = 'account/reset_password.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            check = request.user.check_password(cd['old_password'])
            if check:
                request.user.set_password(cd['new_password'])
                request.user.save()
                messages.success(request, 'password changed successfully', 'success')
                return redirect('home:home')
            messages.error(request, 'old password is wrong', 'danger')
            return redirect('home:home')


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class UserPasswordConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_confirm_form.html'
    success_url = reverse_lazy('account:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html/'


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.error(request, 'user is already followed', 'danger')
        else:
            Relation(from_user=request.user, to_user=user).save()
            messages.success(request, 'user followed', 'success')
        return redirect('account:user_profile', user_id)


class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'user unfollowed', 'success')
        return redirect('account:user_profile', user.id)



class EditUserView(LoginRequiredMixin, View):
    form_class = EditUserForm

    def get(self, request):
        form = self.form_class(instance=request.user.profile,
                               initial={'email': request.user.email})
        return render(request, 'account/edit_profile.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'profile edited', 'success')
        return redirect('account:user_profile', request.user.id)
