"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
import json
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests
from pprint import pprint
from dotenv import load_dotenv
import os

load_dotenv()
IAM_API_KEY = os.getenv("IAM_API_KEY")
COUCH_USERNAME = os.getenv("COUCH_USERNAME")
COUCH_URL = os.getenv("COUCH_URL")
BBDD1 = os.getenv("BBDD1")
BBDD2 = os.getenv("BBDD2")
dealerId = os.getenv("dealerId")

param_dict = {
    "IAM_API_KEY": IAM_API_KEY,
    "COUCH_USERNAME": COUCH_USERNAME,
    "COUCH_URL": COUCH_URL,
    "BBDD1": BBDD1,
    "BBDD2": BBDD2,
    "dealerId": 20
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


def main(params_dic):
    client = Cloudant.iam(
        account_name=params_dic["COUCH_USERNAME"],
        api_key=params_dic["IAM_API_KEY"],
        connect=True,
    )
    db = client[params_dic["BBDD1"]]
    reviews = []
    for doc in db:
        reviews.append(doc)
    # print(reviews)
    client.disconnect()
    return json.dumps(reviews)
