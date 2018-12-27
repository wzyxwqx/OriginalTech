from django.views import generic


class WelcomeView(generic.TemplateView):
    template_name = 'ecoinfor/pagejump.html'
    pass
