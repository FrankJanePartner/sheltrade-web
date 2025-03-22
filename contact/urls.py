"""
URL Configuration for the Contact App.

This module defines the URL patterns for handling contact-related requests.
It includes paths for displaying the contact form, handling form submissions, and viewing contact details.

Routes:
- `/` → Displays the contact form page.
- `/sendContact/` → Handles the submission of the contact form.
- `/contact_detail/` → Displays details of a specific contact message.

The `app_name` variable is set to `contact` to allow namespacing of URLs in templates and views.
"""

from django.urls import path
from .views import contactus, sendContact, contact_detail

# Define the app name for namespacing in Django templates and views
app_name = 'contact'

# URL patterns for the contact application
urlpatterns = [
    path('', contactus, name='contact'),  # Route for displaying the contact form page
    path('sendContact/', sendContact, name='sendContact'),  # Route for handling contact form submission
    path('contact_detail/', contact_detail, name='contact_detail')  # Route for displaying contact message details
]
