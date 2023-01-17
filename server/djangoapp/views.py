from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact_us.html')


def login_form(request):
    # si el usuario esta logeado lo redirige a la pagina principal
    if request.user.is_authenticated:
        return redirect('djangoapp:index')
    return render(request, 'djangoapp/login.html')


# Create a `login_request` view to handle sign in request
def login_request(request):
    context_data = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/login.html', context_data)
    else:
        # if not, return index page
        return render(request, 'djangoapp/index.html', context_data)

        # Create a `logout_request` view to handle sign out request


def logout_request(request):
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

    # Update the `get_dealerships` view to render the index page with a list of dealerships


def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/00a60eeb-e747-42f8-a198-46f636c325a2/dealership-package/get-dealership.json"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        print(dealerships)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/00a60eeb-e747-42f8-a198-46f636c325a2/dealership-package/dealer-id.json"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        #  convert review objejct to json
        reviews = json.dumps(reviews, default=lambda o: o.__dict__)

        return HttpResponse(reviews)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

def add_review(request, dealer_id):
    if request.method == "GET":
        if request.user.is_authenticated:
            review = {}
            review["id"] = request.user.id
            review["name"] = "prueba final"
            review["dealership"] = dealer_id
            review["review"] = "this is a test review"
            review["purchase"] = "false"
            review["purchase_date"] = "10/20/2020"
            review["car_make"] = "subaru"
            review["car_model"] = "subaru"
            review["car_year"] = 2020
            url = "https://us-south.functions.appdomain.cloud/api/v1/web/00a60eeb-e747-42f8-a198-46f636c325a2/dealership-package/post-review.json"

            # Get dealers from the URL
            post_review = post_request(url, review)
            #  convert review objejct to json
            post_review = json.dumps(post_review, default=lambda o: o.__dict__)
            return HttpResponse(post_review)
        else:
            return HttpResponse("User not authenticated")


"""
review = {}
review["id"] = request.user.id
review["name"] = request.user.username
review["dealership"] = dealer_id
review["review"] = request.POST['content']
review["purchase"] = request.POST['purchasecheck']
review["purchase_date"] = request.POST['purchasedate']
review["car_make"] = request.POST['car']
review["car_model"] = request.POST['model']
review["car_year"] = request.POST['year']
url = "https://us-south.functions.appdomain.cloud/api/v1/web/00a60eeb-e747-42f8-a198-46f636c325a2/dealership-package/post-review.json"

"""
