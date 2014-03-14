from django.views.generic import TemplateView


class AdminPanel(TemplateView):
    template_name = "site_manager/main_panel.html"
