from django import forms

class UploadImageForm(forms.Form):
    title = forms.CharField(required=False)
    private = forms.BooleanField(required=False)
    image = forms.ImageField()

    # Size check
    def clean_image(self):
        image = self.cleaned_data['image']
        if image._size > 4 * 1024 * 1024:
            raise forms.ValidationError("Image is too large! Maximium allowed size is 4MB.")
        return image
