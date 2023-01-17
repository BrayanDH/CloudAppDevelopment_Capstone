import json
from cloudant.client import Cloudant
from dotenv import load_dotenv
import os

load_dotenv()
IAM_API_KEY = os.getenv('IAM_API_KEY')
COUCH_USERNAME = os.getenv('COUCH_USERNAME')
COUCH_URL = os.getenv('COUCH_URL')
BBDD1 = os.getenv('BBDD1')
BBDD2 = os.getenv('BBDD2')
dealerId = os.getenv('dealerId')


dict = {
    "IAM_API_KEY": IAM_API_KEY,
    "COUCH_USERNAME": COUCH_USERNAME,
    "COUCH_URL": COUCH_URL,
    "BBDD1": BBDD1,
    "BBDD2": BBDD2,
    "dealerId": 20
}


def main(dict):
    client = Cloudant.iam(
        account_name=dict["COUCH_USERNAME"],
        api_key=dict["IAM_API_KEY"],
        connect=True,
    )
    db = client[dict["BBDD1"]]
    reviews = []
    for doc in db:
        reviews.append(doc)
    # print(reviews)
    client.disconnect()
    return {"data": json.dumps(reviews)}


print(main(dict))
