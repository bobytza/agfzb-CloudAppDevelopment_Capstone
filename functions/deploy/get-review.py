"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests


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
        print(param_dict)
        
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}
        
    # id1=param_dict.get('test')
    # return {"body": id1}
        
    db_name = "reviews"
    db = client[db_name]

    # Fetch all records from the "reviews" database
    records = [doc for doc in db]
    
    dealerId = param_dict.get('dealerId')
    
    if dealerId is not None:
        result_object = next((obj for obj in records if obj.get("id") == int(dealerId)), None)
        print(result_object)
        return {"body": [result_object]}
    else:
        # You can now process the records or return them as needed
        return {"body": records}

    #return {"dbs": client.all_dbs()}
