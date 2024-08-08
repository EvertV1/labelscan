import requests
import streamlit as st
import pandas as pd
import requests

####################################################
# api client
####################################################
# FastAPI server URLs
FASTAPI_PRODUCT_URL = "https://europe-west1-fnacvdb.cloudfunctions.net/whatsapp_handler/get_product_dataframe"
FASTAPI_USERS_URL = "https://europe-west1-fnacvdb.cloudfunctions.net/whatsapp_handler/get_users_dataframe"
FASTAPI_MODEL_URL = "https://europe-west1-fnacvdb.cloudfunctions.net/whatsapp_handler/get_model_dataframe"
FASTAPI_ADD_USER_URL = "https://europe-west1-fnacvdb.cloudfunctions.net/whatsapp_handler/add_user"
FASTAPI_REMOVE_USER_URL = "https://europe-west1-fnacvdb.cloudfunctions.net/whatsapp_handler/remove_user"
FASTAPI_CHECK_MANAGER_URL = "https://europe-west1-fnacvdb.cloudfunctions.net/whatsapp_handler/check_manager"
FASTAPI_MESSAGE_USER_URL = "https://europe-west1-fnacvdb.cloudfunctions.net/whatsapp_handler/message_user"

# Fetch data from FastAPI
def fetch_data_from_fastapi(url):
    """
       Fetch data from a FastAPI endpoint.

       Args:
           url (str): The URL of the FastAPI endpoint.

       Returns:
           dict: The JSON response data from the FastAPI endpoint, or an empty dictionary if an error occurs.
       """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return data
    except requests.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return []

# Send new user data to FastAPI
def send_user_to_fastapi(user_name, user_phone):
    """
        Send user data to a FastAPI endpoint.

        Args:
            user_name (str): The name of the user.
            user_phone (str): The phone number of the user.

        Returns:
            dict: The JSON response data from the FastAPI endpoint, or an empty dictionary if an error occurs.
        """
    try:
        response = requests.post(FASTAPI_ADD_USER_URL, json={"user_name": user_name, "user_phone": user_phone})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error sending data to FastAPI: {e}")
        return {}


def fetch_product_data():
    # Fetch initial data from FastAPI
    product_data = fetch_data_from_fastapi(FASTAPI_PRODUCT_URL)

    # Initialize DataFrames from fetched data
    df_product = pd.DataFrame(product_data['products'])

    return df_product


def fetch_user_data():
    # Fetch initial data from FastAPI
    users_data = fetch_data_from_fastapi(FASTAPI_USERS_URL)

    # Initialize DataFrames from fetched data
    df_users = pd.DataFrame(users_data['users'])

    return df_users


def fetch_model_data():
    # Fetch initial data from FastAPI
    models_data = fetch_data_from_fastapi(FASTAPI_MODEL_URL)

    # Initialize DataFrames from fetched data
    df_models = pd.DataFrame(models_data['models'])

    return df_models

def users_data_to_select_removal():
    # Fetch user data from FastAPI to get the list of users
    df_users = fetch_user_data()

    # Create a list of users with id, name, and phone number
    user_list = [f"{row['user_id']}; {row['user_name']}; {row['user_phone']}" for index, row in df_users.iterrows()]

    return user_list

def remove_user_from_database(user_to_remove):
    # Extract the user ID from the selected value
    user_id_to_remove = user_to_remove.split(";")[0]
    print(user_id_to_remove)
    try:
        response = requests.post(FASTAPI_REMOVE_USER_URL, json={"user_id": str(user_id_to_remove)})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error sending data to FastAPI: {e}")
    return None

def check_manager(name, password):
    response = requests.post(FASTAPI_CHECK_MANAGER_URL, json={"manager_name": name, "manager_password": password})
    manager_access = response.json().get('manager_access', False)
    return manager_access

def send_whatsapp_message(user_to_message):
    # Extract the user ID from the selected value
    user_number_to_message = user_to_message.split(";")[2]
    user_name = user_to_message.split(";")[1]
    print(user_number_to_message)
    print(user_name)
    try:
        response = requests.post(FASTAPI_MESSAGE_USER_URL, json={"user_number": str(user_number_to_message),
                                                                 "user_name": str(user_name)})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error sending data to api server: {e}")
    return None