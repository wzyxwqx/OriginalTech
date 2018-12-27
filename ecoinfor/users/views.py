from .forms import RegisterForm
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.urls import reverse

# Create your views here.


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/users/registration_success/'

    def get_success_url(self):
        next_url = self.request.POST.get('next', self.request.GET.get('next', ''))
        if (next_url):
            return '%s' % (next_url)
        else:
            return '/'
        
    def form_valid(self, form):
        form.send_email()
        form.save()
#        RegisterView.
        return super().form_valid(form)


class SuccessView(TemplateView):
    template_name = 'success.html'
