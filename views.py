from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from imgup.forms import UploadImageForm
from imgup.models import Image, ImageUser

# Front page, list 40 of the latest non-private images
def index(request):
	images = Image.objects.filter(private=False).order_by('-datetime')[:40]
	return render(request, 'base_imgup_index.html', {'images': images})

# Handling user logins, returns HTTP status codes for the JavaScript to interpret
# Creates a new ImageUser extension for the logging user if one doesn't already exist
def user_login(request):
	usern = request.POST['username']
	passw = request.POST['password']
	user = authenticate(username=usern, password=passw)
	if user is not None:
	    if user.is_active:
	        login(request, user)
	        imguser = ImageUser.objects.filter(user=user)
	        if imguser.count() == 0:
	        	iu = ImageUser(user=user)
	        	iu.save()
	        return HttpResponse(status=200)
	    else:
	        return HttpResponse(status=401)
	else:
	    return HttpResponse(status=401)

# Logging out
def user_logout(request):
	logout(request)
	return HttpResponse(status=200)

# Write uploaded file to disk
def handle_uploaded_file(file_path):
	dest = open(file_path.name, "wb")
	for chunk in file_path.chunks():
		dest.write(chunk)
	dest.close()

# Displays the upload form or processes it if it has been sent.
def upload_file(request):
	iu = ImageUser.objects.get(user=request.user)
	usedspace = iu.current_total_size / 1024
	totalspace = iu.max_total_size / 1024
	if request.method == 'POST':
		success = False
		form = UploadImageForm(request.user, request.POST, request.FILES)
		if form.is_valid():
			imgfile = request.FILES["image"]
			handle_uploaded_file(imgfile)
			i = Image(
				uploader = request.user,
				title = request.POST['title'],
				private = request.POST.get('private', False),
				img = imgfile,
				)
			i.save()
			iu.current_total_size += imgfile._size/1024
			iu.save()
			success = True
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

# Default profile view, displays latest non-private uploads by the user
# !!! NOT YET IMPLEMENTED !!!
def profile_view_index(request):
	if request.user.is_authenticated:
		return render(request, "base_imgup_profile.html")
	else:
		return HttpResponseRedirect("/imgup/")