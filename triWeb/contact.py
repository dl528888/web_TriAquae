from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from django import forms

class ContactForm(forms.Form):
        subject = forms.CharField()
        email   = forms.EmailField(required=False, label ="Your email address:")
        message = forms.CharField(widget=forms.Textarea)


def Contact(request):
	if request.method == 'POST':
		form = ContactForm(request.Form)
		if form.is_valid():
			cd =  form.cleaned_data
			send_mail(
                          cd['subject'],
                          cd['message'],
                          cd.get('email','noreply@example.com'),
                          ['triaquae@gmail.com'],

			)
		return HttpResponseRedirect('/contact/thanks/')
	else:
		form = ContactForm()
	return render_to_response('contact_form.html',{'form':form})

def contacts(request):
	errors = []
	
	if request.method == 'POST':
		if not request.POST.get('subject',''):
			errors.append('Enter a subject.')
		if not request.POST.get('message',''):
			errors.append('Enter a message.')
		if request.POST.get('email') and '@' not in request.POST['email']:
			errors.append('Enter a valid e-mail address')
		if not errors:
			send_mail(

				request.POST['subject'],
				request.POST['message'],
				request.POST.get('email','noreply@example.com'),
				['triaquae@gmail.com'],
			)
		return HttpResponseRedirect('/contact/thanks/')
	return render_to_response('contact.html',{'error':errors})

