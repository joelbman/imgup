from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from imgup.forms import UploadImageForm
from imgup.models import Image, ImageUser

# Front page, list 40 of the latest non-private images
def index(request):
	images = Image.objects.filter(private=False).order_by('-datetime')[:40]
	return render(request, 'base_imgup_index.html', {'images': images})

# Handling user logins, returns HTTP status codes for the JavaScript to interpret
def user_login(request):
	usern = request.POST['username']
	passw = request.POST['password']
	user = authenticate(username=usern, password=passw)
	if user is not None:
	    if user.is_active:
	        login(request, user)
	        return HttpResponse(status=200)
	    else:
	        return HttpResponse(status=401)
	else:
	    return HttpResponse(status=401)

# Logging out
def user_logout(request):
	logout(request)
	return HttpResponse(status=200)

# Displays the upload form or processes it if it has been sent.
# If the user has no ImageUser object, create one.
def upload_file(request):
	while True:
		try:
			iu = ImageUser.objects.get(user=request.user)
			break;
		except ImageUser.DoesNotExist:
			iu = ImageUser(user=request.user)
			iu.save()
	usedspace = round(float(iu.current_total_size) / 1024.0, 1)
	totalspace = round(float(iu.max_total_size) / 1024.0, 1)
	if request.method == 'POST':
		success = False
		form = UploadImageForm(request.user, request.POST, request.FILES)
		if form.is_valid():
			imgfile = request.FILES["image"]
			i = Image(
				uploader = request.user,
				private = request.POST.get('private', False),
				img = imgfile,
				)
			i.save()
			iu.current_total_size += imgfile._size/1024
			iu.save()
			success = True
			usedspace += round(imgfile._size / 1024.0 / 1024.0, 1)
		return render(request, "base_imgup_upload.html", {
			"form": form,
			"success": success,
			"usedspace": usedspace,
			"totalspace": totalspace
			})
	else:
		form = UploadImageForm(request.user)
		return render(request, "base_imgup_upload.html", {
			"form": form,
			"usedspace": usedspace,
			"totalspace": totalspace
			})

# Profile view, displays latest non-private uploads by the user
# If the user is logged in and viewing his/her own profile, private images are also shown.
def profile_view(request, *args, **kwargs):
	if ("user_name" in kwargs):
		user_name = kwargs["user_name"]
		user = get_object_or_404(User, username=user_name)
		owner = False
		if request.user.is_authenticated and request.user == user:
			images = Image.objects.filter(uploader=user).order_by("-datetime")
			owner = True
		else:
			images = Image.objects.filter(uploader=user, private=False).order_by("-datetime")

		return render(request, "base_imgup_profile.html", {
			"images": images,
			"user": user,
			"owner": owner
			})
	else:
		if request.user.is_authenticated:
			return HttpResponseRedirect("/imgup/user/" + request.user.username + "/")
		else:
		 	return HttpResponseRedirect("/imgup/")

# Delete requested image from the database and filesystem and
# subtract the image size from the user's current disk usage
def delete_image(request, image_id):
	if request.user.is_authenticated:
		img = get_object_or_404(Image, pk=image_id)
		if request.user == img.uploader:
			iu = get_object_or_404(ImageUser, user=request.user)
			iu.current_total_size -= img.img.size / 1024
			iu.save()
			img.img.delete()
			img.delete()
			return HttpResponseRedirect("/imgup/user/")
	else:
		return HttpResponseRedirect("/imgup/")