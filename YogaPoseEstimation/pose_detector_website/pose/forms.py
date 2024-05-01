from django import forms

class UploadForm(forms.Form):
    image = forms.ImageField(label='Upload your Yoga Pose')

class CaptureForm(forms.Form):
    image = forms.ImageField(label='Upload your Yoga Pose')