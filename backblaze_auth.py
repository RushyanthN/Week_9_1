import os
from b2sdk.v2 import B2Api
from dotenv import load_dotenv
load_dotenv()

def authorize_b2_account():
    b2 = B2Api()
    application_key_id = os.getenv('keyID')
    application_key = os.getenv('applicationKey')

    try:
        b2.authorize_account("production", application_key_id, application_key)
        print("Authorization successful")
        return b2
    except Exception as e:
        print("Authorization failed:", e)
        return None

if __name__ == "__main__":
    authorize_b2_account()
