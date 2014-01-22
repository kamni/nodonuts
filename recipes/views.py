from django.views.generic import TemplateView


class Home(TemplateView):
    def get(self, request, *args, **kwargs):
        from django.http import HttpResponse
        return HttpResponse('home')
