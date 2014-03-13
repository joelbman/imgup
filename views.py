from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from imgup.forms import UploadImageForm
from imgup.models import Image

# Front page, list 40 of the latest non-private images
def index(request):
	q = Image.objects.filter(private=False).order_by('-datetime')[:40]
	return render(request, 'base_imgup_index.html', {'images': q})

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

# Write uploaded file to disk
def handle_uploaded_file(file_path):
    dest = open(file_path.name, "wb")
    for chunk in file_path.chunks():
        dest.write(chunk)
    dest.close()

# Displays the upload form or processes it if it has been sent.
def upload_file(request):
	if request.method == 'POST':
		form = UploadImageForm(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES["image"])
			i = Image(
				uploader = request.user,
				title = request.POST['title'],
				private = request.POST.get('private', False),
				img = request.FILES["image"]
				)
			i.save()
		return render(request, "base_imgup_upload.html", {"form": form })
	else:
		form = UploadImageForm()
		return render(request, "base_imgup_upload.html", {"form": form })

# Default profile view, displays latest non-private uploads by the user
# !!! NOT YET IMPLEMENTED !!!
def profile_view_index(request):
	if request.user.is_authenticated:
		return render(request, "base_imgup_profile.html")
	else:
		return HttpResponseRedirect("/imgup/")