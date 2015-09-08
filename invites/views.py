from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.crypto import get_random_string
from django.shortcuts import (
    get_object_or_404,
    redirect,
)
from django.views.generic import (
    CreateView,
    FormView,
    View,
)

from libraries.models import (
    Library,
    Librarian,
)
from .models import Invitation
from .forms import InvitationForm


class CreateInviteView(CreateView):

    model = Invitation
    form_class = InvitationForm
    template_name = 'invite_edit.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect(
                '{}?next={}'.format(settings.LOGIN_URL, request.path)
            )
        return super(CreateInviteView, self).dispatch(request, *args, **kwargs)


    def get_success_url(self, **kwargs):
        return reverse('book-list')

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.library = Librarian.objects.get(
            user=self.request.user,
        ).library
        messages.success(
            self.request,
            "Invited {}".format(form.cleaned_data.get('email')),
        )
        return super(CreateInviteView, self).form_valid(form)


class AcceptInviteView(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            messages.warning(
                self.request,
                "Logged-in users can't accept invitations",
                )
            return redirect(reverse('book-list'))
        invite = get_object_or_404(
            Invitation.objects,
            key=kwargs.get('key'),
            status=Invitation.SENT,
        )
        # By this point we should have a good invite.
        password_plain = get_random_string(20)
        password = make_password(password_plain)
        user = User.objects.create(
            username=invite.email,
            email=invite.email,
            password=password,
        )
        user.save()
        user = authenticate(username=invite.email, password=password_plain)
        if invite.library:
            Librarian.objects.create(user=user, library=invite.library)
        else:
            library = Library.objects.create(title="{}'s library".format(user))
            Librarian.objects.create(user=user, library=library)
        login(request, user)
        invite.status = invite.ACCEPTED
        invite.save()
        messages.success(
            self.request,
            "Account created, please change your password!",
        )
        return redirect(reverse('set-password'))


class ChangePasswordView(FormView):

    form_class = SetPasswordForm
    template_name = "set_password.html"

    def get_success_url(self):
        return reverse('book-list')

    def get_form(self):
        return self.form_class(self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        messages.success(
            self.request,
            "Welcome to Booksonas!",
        )
        return super(ChangePasswordView, self).form_valid(form)
