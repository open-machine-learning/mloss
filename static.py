from django.shortcuts import render_to_response
import pdb

def faq(request):
	print "faq"
	return render_to_response('faq.html')

def links(request):
    return render_to_response('links.html')

def about(request):
    return render_to_response('about.html')

def workshop(request):
    return render_to_response('workshop06.html')

