from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):

    def send_email(self):
        pass

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')
