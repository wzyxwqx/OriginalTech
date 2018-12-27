from django.db import models
from django.utils import timezone

# Create your models here.


class Share(models.Model):
	name_text = models.CharField(max_length = 20)
	intro_text = models.CharField(max_length = 1000)
	company_text = models.CharField(max_length = 200)
	hot_index = models.IntegerField()
	def __str__(self):
		return self.name_text


def detail_share(request, share_id):
	try:
		share = Share.objects.get(pk = message_id)
	except Share.DoesNotExist:
		raise Http404("This share does not exist. Please try again later.")
	return render(request, 'share/detail.html', {'share':share})