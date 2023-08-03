from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests

def main(param_dict):
    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )
        print(f"Databases: {client.all_dbs()}")

        # Get the "reviews" database
        db_name = "reviews"
        db = client[db_name]

        # Sample review data to be inserted
        # new_review = {
        #     "title": "Sample Review",
        #     "content": "This is a test review.",
        #     "rating": 5
        # }

        # Create a new document (review) in the "reviews" database
        db.create_document(param_dict.get('review'))
        print("New review created successfully.")

    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"body": param_dict.get('review')}