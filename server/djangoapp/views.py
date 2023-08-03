from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)


# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
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
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/be932420-f3e7-4769-a777-9aed02e58cd2/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)

        context["dealerships"] = dealerships
        print(context)

        return render(request, 'djangoapp/index.html', context)
        # Concat all dealer's short name
        # dealer_names = ' --- '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        # return HttpResponse(dealer_names)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/be932420-f3e7-4769-a777-9aed02e58cd2/dealership-package/get-review"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
        print(reviews)

        context["reviews"] = reviews
        context["dealer_id"] = dealer_id

        return render(request, 'djangoapp/dealer_details.html', context)
        # Concat all dealer's short name
        #reviews_names = ' --- '.join([review.name + "(" + review.sentiment + ")" for review in reviews])
        # Return a list of dealer short name
        #return HttpResponse(reviews_names)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
def add_review(request, dealer_id):
    if request.user.is_authenticated:
        if request.method == "GET":
            context = {}
            context["dealer_id"] = dealer_id
            context["cars"] = CarModel.objects.all()
            url = "https://us-south.functions.appdomain.cloud/api/v1/web/be932420-f3e7-4769-a777-9aed02e58cd2/dealership-package/get-dealership?dealerId=" + str(dealer_id)
            dealer = get_dealers_from_cf(url)
            print(dealer)
            context["dealer"] = dealer[0]
        

            return render(request, 'djangoapp/add_review.html', context)
        if request.method == "POST":
            print("Logged in")
            review=dict()

            review["dealership"] = dealer_id
            review["name"] = "test"
            review["purchase"] = True
            review["review"] = "Best car in the world"
            review["purchase_date"] = datetime.utcnow().isoformat()
            review["car_make"] = "test"
            review["car_model"] = "test"
            review["car_year"] = "test"
            review["sentiment"] = "unknown"
            review["id"] = 10

            print(review)
            post_request("https://us-south.functions.appdomain.cloud/api/v1/web/be932420-f3e7-4769-a777-9aed02e58cd2/dealership-package/post-review", {"review": review}, dealerId=dealer_id)

            # Return a list of dealer short name
            return JsonResponse(review)
    else:
        print("Not logged in")


