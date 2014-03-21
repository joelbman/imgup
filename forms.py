from django import forms
from imgup.models import ImageUser

class UploadImageForm(forms.Form):

	image = forms.ImageField()
	private = forms.BooleanField(required=False)
	
	# Override the initialization so request.user can be passed
	def __init__(self, usern, *args, **kwargs):
		super(UploadImageForm, self).__init__(*args, **kwargs)
		self.user = usern

	# Size check
	def clean_image(self):
		image = self.cleaned_data['image']
		imguser = ImageUser.objects.get(user=self.user)
		if image._size/1024 > imguser.max_file_size:
			raise forms.ValidationError(
				"Image is too large! Maximium allowed size is " 
				+ str(imguser.max_file_size/1024) + "MB."
				" The image was " + str(image._size/1024/1024) + "MB"
				)
		if imguser.current_total_size + image._size/1024 > imguser.max_total_size:
			raise forms.ValidationError("You have reached the total upload limit.")
		return image
