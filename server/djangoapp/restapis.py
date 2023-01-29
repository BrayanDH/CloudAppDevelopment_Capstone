import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv('api_key')


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if api_key:
            response = requests.get(url, params=kwargs, headers={
                'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, params=kwargs, headers={
                                    'Content-Type': 'application/json'})
    except:
        # If any error occurs
        print("Network exception occurred")

    # Retrieve HTTP response status code and parse response data from JSON to Python dictionary
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    try:
        # Call post method of requests library with URL, parameters and data
        response = requests
        if api_key:
            response = requests.post(url, params=kwargs, json=json_payload, headers={
                                     'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.post(url, params=kwargs, json=json_payload, headers={
                                     'Content-Type': 'application/json'})
    except:
        # If any error occurs
        print("Network exception occurred")

    # Retrieve HTTP response status code and parse response data from JSON to Python dictionary
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter and get the returned JSON result
    json_result = get_request(url)
    if json_result:
        dealers = json_result["data"]

        for dealer in dealers:
            # Get its content in `doc` object and create a CarDealer object with values in `doc` object and append it to the results list
            dealer_doc = dealer["doc"]
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], state=dealer_doc["state"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    # Call get_request with a URL parameter
    json_result = get_request(
        "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/67e6e456-38ad-4522-bc0d-e80e28e70226/v1/analyze?version=2020-08-01", text=text, features="sentiment")

    # Get the returned sentiment label such as Positive or Negative
    if json_result:
        sentiment = json_result["sentiment"]["document"]["label"]
        return sentiment
    else:

        return "Neutral"


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter and get the returned JSON result
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        reviews = json_result["reviews"]

        # Get its content in `doc` object and create a DealerReview object with values in `doc` object and append it to the results list
        for review in reviews:
            review_doc = review
            text = review_doc["review"]
            sentiment = analyze_review_sentiments(text)

            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(dealership=review_doc["dealership"], name=review_doc["name"],
                                      purchase=review_doc["purchase"], review=review_doc["review"],
                                      purchase_date=review_doc["purchase_date"], car_make=review_doc["car_make"],
                                      car_model=review_doc["car_model"], car_year=review_doc["car_year"],
                                      sentiment=sentiment, id=review_doc["id"])
            results.append(review_obj)

    return results


"""
# test get_dealer_reviews_from_cf funtion
result = get_dealer_reviews_from_cf(
    "https://us-south.functions.appdomain.cloud/api/v1/web/00a60eeb-e747-42f8-a198-46f636c325a2/dealership-package/dealer-id.json", 20)
"""

"""
#test get_request funtion
response = get_request(
    "https://us-south.functions.appdomain.cloud/api/v1/web/00a60eeb-e747-42f8-a198-46f636c325a2/dealership-package/get-dealership.json" )
 print(response)
"""

"""
#test get_dealers_from_cf funtion
result = get_dealers_from_cf(
    "https://us-south.functions.appdomain.cloud/api/v1/web/00a60eeb-e747-42f8-a198-46f636c325a2/dealership-package/get-dealership.json")
"""


"""test post request

dealer_id = 20
review = {}
review["id"] = "10"
review["name"] = "nombre prueba"
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
print(post_review)
"""
