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

	def rename(path):
		def wrapper(instance, filename):
			import hashlib
			from datetime import datetime
	
			ext = filename.split(".")[-1]
			ihash = hashlib.md5(str(datetime.now().microsecond)).hexdigest()[0:8]

			new_filename = ihash + "." + ext
			full_path = path + new_filename

			return full_path
		return wrapper

	datetime = models.DateTimeField(auto_now_add = True)
	img = ImageField(upload_to=rename("imgup/"))
	private = models.BooleanField(default=False)
	title = models.CharField(max_length=30, default="")
	uploader = models.ForeignKey(User)

	def __unicode__(self):
		return self.img