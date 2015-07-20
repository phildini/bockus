from django.views.generic import TemplateView
from books.views import BookListView


class HomeView(TemplateView):

    template_name = "home.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return BookListView.as_view()(request)

        return super(HomeView, self).dispatch(request, *args, **kwargs)

