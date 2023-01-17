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
    # Crear un nuevo documento
    new_doc = {
        "id": 6,
        "name": dict["name"],
        "dealership": dict["dealership"],
        "review": dict["review"],
        "purchase": dict["purchase"],
        "purchase_date": dict["purchase_date"],
        "car_make": dict["car_make"],
        "car_model": dict["car_model"],
        "car_year": dict["car_year"]
    }
    db.create_document(new_doc)

    # Desconectarse de Cloudant
    client.disconnect()

    # Devolver el id del nuevo documento
    return {"body": json.dumps({"id": new_doc["id"]})}
