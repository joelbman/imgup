from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField

# Extended user class, holds the upload limitations
# !!! NOT IMPLEMENTED YET !!!
class ImageUser(models.Model):
	user = models.OneToOneField(User)
	max_file_size = models.IntegerField(default=4096)
	max_total_size = models.IntegerField(default=102400)

	def __unicode__(self):
		return self.user

class Image(models.Model):
	img = ImageField(upload_to="imgup/")
	title = models.CharField(max_length=30, default="")
	uploader = models.ForeignKey(User)
	private = models.BooleanField(default=False)
	datetime = models.DateTimeField(auto_now_add = True)

	def __unicode__(self):
		return self.img