from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarMake, CarModel, CarDealer, DealerReview
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from datetime import datetime

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact_us.html')


# Create a `add_review` view to submit a review
def login_form(request):
    # If user is already logged in, redirect user to index page
    if request.user.is_authenticated:
        return redirect('djangoapp:index')
    return render(request, 'djangoapp/login.html')


# Create a `login_request` view to handle sign in request
def login_request(request):

    # Get username and password from request.POST dictionary
    context_data = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)

        # Check if user exist, if yes, sign in user, if not return to login page again
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/login.html', context_data)
    else:
        # if not, return index page
        return render(request, 'djangoapp/index.html', context_data)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Logout user in the request and redirect user to login page
    logout(request)
    return redirect('djangoapp:index')


def registration_request(request):
    # Create a `registration_request` view to handle sign up request
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists in database and create user if not exist
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

        # If user does not exist, create user and sign in user, if user exists, return to registration page
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
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/00a60eeb-e747-42f8-a198-46f636c325a2/dealership-package/get-dealership.json"

        # Get dealers from the URL and pass it to the context
        dealerships = get_dealers_from_cf(url)
        context = {"dealerships": dealerships}
        return render(request, 'djangoapp/index.html', context)

        # print(dealerships)
        # # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # # Return a list of dealer short name
        # return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id, dealer_name):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/00a60eeb-e747-42f8-a198-46f636c325a2/dealership-package/dealer-id.json"
        # Get dealers from the URL and get reviews by dealer id
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context = {"reviews": reviews, "dealer_id": dealer_id,
                   "dealer_name": dealer_name}
        return render(request, 'djangoapp/dealer_details.html', context)
        # #  convert review objejct to json
        # reviews = json.dumps(reviews, default=lambda o: o.__dict__)

        # return HttpResponse(reviews)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id, dealer_name):
    # If request is GET, render the add review form page
    if request.method == "GET":
        if request.user.is_authenticated:
            context = {}
            cars = CarModel.objects.all()
            context = {"cars": cars, "dealer_id": dealer_id,
                       "dealer_name": dealer_name}
            return render(request, 'djangoapp/add_review.html', context)
        else:
            # If not, return index page
            return redirect('djangoapp:login')

    # If request is POST, get form data and save it to database
    if request.method == "POST":
        if request.user.is_authenticated:
            car = CarModel.objects.get(id=request.POST.get("car"))
            review = {}
            review["id"] = request.user.id
            review["name"] = request.user.username
            review["dealership"] = dealer_id
            review["review"] = request.POST.get("content")
            review["purchase"] = request.POST.get("purchasecheck")
            review["purchase_date"] = request.POST.get("purchasedate")
            review["car_make"] = car.car_make.name
            review["car_model"] = car.name
            review["car_year"] = car.year.strftime("%Y")
            url = "https://us-south.functions.appdomain.cloud/api/v1/web/00a60eeb-e747-42f8-a198-46f636c325a2/dealership-package/post-review.json"

            # Get dealers from the URL and convert review object to json
            post_review = post_request(url, review)
            post_review = json.dumps(post_review, default=lambda o: o.__dict__)
            return redirect("djangoapp:dealer_details",
                            dealer_id=dealer_id, dealer_name=dealer_name)
