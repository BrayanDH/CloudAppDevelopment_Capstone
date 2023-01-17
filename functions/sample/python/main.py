"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
import json
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests
from pprint import pprint
param_dict = {
    "COUCH_URL": "https://4648c3fb-249c-432b-91b8-dbeedf0a2409-bluemix.cloudantnosqldb.appdomain.cloud",
    "IAM_API_KEY": "sleg24V72V8xtJ9-l2vXIsO0AVf1kHHUl8L-zGPvQj4V",
    "COUCH_USERNAME": "4648c3fb-249c-432b-91b8-dbeedf0a2409-bluemix"
}


def main(param_dict):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """

    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )
        print(f"Databases: {client.all_dbs()}")
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}


# print(main(param_dict))


def get_reviews(account, api_key, database):
    client = Cloudant.iam(account, api_key)
    client.connect()
    db = client[database]
    reviews = []
    for doc in db:
        reviews.append(doc)
    # print(reviews)
    client.disconnect()
    return json.dumps(reviews)


result = get_reviews(param_dict["COUCH_USERNAME"],
                     param_dict["IAM_API_KEY"], "reviews")
pprint(result)


def main(dict):
    client = Cloudant.iam(
        account_name=dict["COUCH_USERNAME"],
        api_key=dict["IAM_API_KEY"],
        connect=True,
    )
    db = client[dict["DATABASE"]]
    reviews = []
    for doc in db:
        reviews.append(doc)
    # print(reviews)
    client.disconnect()
    return json.dumps(reviews)


{
    "COUCH_URL": "https://4648c3fb-249c-432b-91b8-dbeedf0a2409-bluemix.cloudantnosqldb.appdomain.cloud",
    "IAM_API_KEY": "sleg24V72V8xtJ9-l2vXIsO0AVf1kHHUl8L-zGPvQj4V",
    "COUCH_USERNAME": "4648c3fb-249c-432b-91b8-dbeedf0a2409-bluemix",
    "DATABASE": "reviews"
}
