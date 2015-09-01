from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import (
    get_object_or_404,
    redirect,
)
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from readers.models import Reader

class UserOwnedObjectMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(
                '{}?next={}'.format(settings.LOGIN_URL, request.path)
            )

        return super(UserOwnedObjectMixin, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(UserOwnedObjectMixin, self).get_queryset()
        queryset = queryset.filter(
            user=self.request.user
        )
        return queryset

    def get_object(self, queryset=None):
        instance = super(UserOwnedObjectMixin, self).get_object(queryset)

        if not instance.user == self.request.user:
            raise PermissionDenied

        return instance


class ReaderListView(UserOwnedObjectMixin, ListView):

    model = Reader
    template_name = "reader_list.html"


class ReaderView(UserOwnedObjectMixin, DetailView):

    model = Reader
    template_name = "reader.html"


class CreateReaderView(UserOwnedObjectMixin, CreateView):

    model = Reader
    template_name = "reader_edit.html"
    fields = ['kind', 'email']

    def get_success_url(self):
        if self.request.POST.get('next'):
            return self.request.POST.get('next')
        return reverse('reader-list')

    def get_context_data(self, **kwargs):
        context = super(CreateReaderView, self).get_context_data(**kwargs)
        if self.request.GET.get('next'):
            context['next'] = self.request.GET.get('next')
        context['action'] = reverse('reader-create')

        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super(CreateReaderView, self).form_valid(form)
        self.object.name = "{}'s {}".format(
            self.object.user, self.object.kind,
        )
        self.object.save()
        return response


class EditReaderView(UserOwnedObjectMixin, UpdateView):

    model = Reader
    template_name = "reader_edit.html"
    fields = ['name', 'kind', 'email']

    def get_success_url(self):
        return reverse(
            'reader-detail',
            kwargs={'pk': self.object.id}
        )

    def get_context_data(self, **kwargs):
        context = super(EditReaderView, self).get_context_data(**kwargs)
        context['action'] = reverse(
            'reader-edit',
            kwargs={'pk': self.object.id},
        )

        return context

    def form_valid(self, form):
        messages.success(self.request, "{} updated.".format(self.object))
        form.instance.user = self.request.user
        return super(EditReaderView, self).form_valid(form)


class DeleteReaderView(UserOwnedObjectMixin, DeleteView):

    model = Reader
    template_name = "reader_delete.html"

    def get_success_url(self):
        return reverse('reader-list')

    def form_valid(self, form):
        messages.success(self.request, "{} deleted.".format(self.object))

        return super(DeleteReaderView, self).form_valid(form)
