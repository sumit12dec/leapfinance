from django import forms

class LinkForm(forms.Form):
	"""Form for submitting link"""
	link = forms.URLField(label='Link', max_length=1000)