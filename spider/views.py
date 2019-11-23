from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import LinkForm
import boto3

from .models import Reference
from extractor.utils.aws import get_boto_session, ACCESS_KEY_ID, SECRET_ACCESS_KEY
import json
import time

from .utils import get_item, invoke_lambda

def index(request):
	if request.user.is_authenticated:
		return HttpResponse("Hello, world. You've successfully logged in.")

	else:
		return HttpResponse("Please <a href='/accounts/login'>login</a> to continue.")


def get_link(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = LinkForm(request.POST)
		# check whether it's valid:
		context = {"error": "Error Occured. Invalid Request"}
		
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			link = form.cleaned_data['link']
			print(link, "link provided")

			r = Reference.objects.filter(crawled_uri=link)

			if r:
				context = get_item(r[0].url_id)
			else:		
				payload = {"crawled_uri": link}
				r = Reference.objects.create(**payload)
				r.save()
				# session = get_boto_session()

				response = invoke_lambda(link, r.url_id)
				print(response['ResponseMetadata']['RequestId'])
				print("above is request ID")
				
				time.sleep(3)

				context = get_item(r.url_id)
				i = 0
				
				while i < 6:
					time.sleep(1)
					context = get_item(r.url_id)
					
					if "error" not in context:
						break
					i += 1

				print("Response from get_item", context)

			if "error" in context and (context["error"] == "In Process"):
				context["error"] = "Please try again. Request still in process & taking more than 10 seconds."

			print("response to be forward to UI", context)

		return render(request, 'scraped_data.html', context=context)

	# if a GET (or any other method) we'll create a blank form
	else:
		form = LinkForm()

	return render(request, 'submit_link.html', {'form': form})

def scraped_data(request):
	"""View function for home page of site."""
  
	context = {'teams': 1, 'points': 2}

	# Render the HTML template index.html with the data in the context variable
	return render(request, 'scraped_data.html', context=context)


