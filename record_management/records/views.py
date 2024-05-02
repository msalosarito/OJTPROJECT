from venv import logger
from django.shortcuts import render, redirect
from jwt import InvalidTokenError
from .models import UserRecord
from .firebase import db_instance
from firebase_admin import auth
from django.contrib.auth import login as django_login, authenticate
from django.contrib import messages
from .forms import RegistrationForm

from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Registration successful, redirect the user to a login page
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'records/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # User is authenticated, log the user in
            django_login(request, user)
            return redirect('document_list')
        else:
            # Authentication failed, display error message
            messages.error(request, 'Invalid email or password.')
            # You might want to redirect back to the login page with an error message
            # return redirect('login')

    # Render the login page if it's a GET request or authentication fails
    return render(request, 'records/login.html')
def document_list(request):
    user = auth.get_user(request)
    if user:
        try:
            # Get user profile
            user_profile = UserProfile.objects.get(user_id=user.uid)
            role = user_profile.role
        except UserProfile.DoesNotExist:
            # Handle case where user profile does not exist
            logger.error('User profile does not exist for user: %s', user.uid)
            return render(request, 'error.html', {'message': 'User profile does not exist'})

        if role == 'administrative':
            # Fetch all documents
            documents = db_instance.child('documents').get()
        elif role in ['division', 'service']:
            # Fetch documents added by the current user
            documents = db_instance.child('documents').order_by_child('added_by').equal_to(user.uid).get()
        else:
            logger.error('Unknown role for user: %s', user.uid)
            return render(request, 'error.html', {'message': 'Unknown role'})

        return render(request, 'records/document_list.html', {'documents': documents})
    else:
        # User is not authenticated, redirect to login page
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')

def add_document(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES.get('file')

        documents_ref = db_instance.child('documents')
        new_document_ref = documents_ref.push({
            'title': title,
            'file_name': file.name,
            'file_description': "Your file description here"
        })
        
        return redirect('document_list')
    return render(request, 'records/add_document.html')

def edit_document(request, doc_key):  
    document = db_instance.child('documents').child(doc_key).get()
    if request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES.get('file')
        
        db_instance.child('documents').child(doc_key).update({
            'title': title,
           
        })
        
        return redirect('document_list')
    return render(request, 'records/edit_document.html', {'document': document})

def delete_document(request, doc_key):
    if request.method == 'POST':
        db_instance.child('documents').child(doc_key).delete()
        return redirect('document_list')
    return render(request, 'records/delete_document.html', {'doc_key': doc_key})


