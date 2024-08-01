import pandas as pd
import streamlit as st
import requests



####################################################
# api client
####################################################
# FastAPI server URLs
FASTAPI_PRODUCT_URL = "http://localhost:8000/get_product_dataframe"
FASTAPI_USERS_URL = "http://localhost:8000/get_users_dataframe"
FASTAPI_MODEL_URL = "http://localhost:8000/get_model_dataframe"
FASTAPI_ADD_USER_URL = "http://localhost:8000/add_user"

# Fetch data from FastAPI
def fetch_data_from_fastapi(url):
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
    try:
        response = requests.post(FASTAPI_ADD_USER_URL, json={"user_name": user_name, "user_phone": user_phone})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error sending data to FastAPI: {e}")
        return {}



####################################################
# backend gui
####################################################
def app():
    st.title("Backend Data Display")

    # Fetch initial data from FastAPI
    product_data = fetch_data_from_fastapi(FASTAPI_PRODUCT_URL)
    users_data = fetch_data_from_fastapi(FASTAPI_USERS_URL)
    model_data = fetch_data_from_fastapi(FASTAPI_MODEL_URL)


    # Initialize DataFrames from fetched data

    df_product = pd.DataFrame(product_data['products'])
    df_users = pd.DataFrame(users_data['users'])
    df_models = pd.DataFrame(model_data['models'])


    # Add a button to manually check for new data
    if st.button('Check for New Data'):
        # Fetch initial data from FastAPI
        product_data = fetch_data_from_fastapi(FASTAPI_PRODUCT_URL)
        users_data = fetch_data_from_fastapi(FASTAPI_USERS_URL)
        model_data = fetch_data_from_fastapi(FASTAPI_MODEL_URL)

        # Initialize DataFrames from fetched data

        df_product = pd.DataFrame(product_data['products'])
        df_users = pd.DataFrame(users_data['users'])
        df_models = pd.DataFrame(model_data['models'])

    # Add new user to the Users DataFrame
    st.subheader("Add New User")

    with st.form(key='user_form'):
        user_name = st.text_input("User Name")
        user_phone = st.text_input("Phone Number")
        submit_button = st.form_submit_button(label='Add User')

        # submit the new user to the user dataframe
        if submit_button:
            if not user_name or not user_phone:
                st.error("Please enter both user name and phone number.")
            else:
                # Send new user data to FastAPI
                response = send_user_to_fastapi(user_name, user_phone)
                if response:
                    st.success(response.get("message", "User added successfully"))

                    # Fetch  data from FastAPI
                    users_data = fetch_data_from_fastapi(FASTAPI_USERS_URL)

                    # Initialize DataFrame from fetched data
                    df_users = pd.DataFrame(users_data['users'])




    # Convert the 'product_image' and 'receipt_image' columns to clickable links
    if 'product_image' in df_product.columns:
        df_product['product_image'] = df_product['product_image'].apply(lambda x: f'<a href="{x}" target="_blank">View Image</a>')

    if 'receipt_image' in df_product.columns:
        df_product['receipt_image'] = df_product['receipt_image'].apply(lambda x: f'<a href="{x}" target="_blank">View Receipt</a>')

    options = ['user_dataframe', 'products_dataframe', 'models_dataframe']
    selected_dataframe = st.selectbox('choose an option', options)

    if selected_dataframe == options[1]:

        # Display the updated DataFrames with clickable links and centered headers
        st.write("Products DataFrame:")
        st.write(df_product.to_html(escape=False, index=False), unsafe_allow_html=True)

    if selected_dataframe == options[2]:
        st.write("Models Dataframe:")
        st.write(df_models)

    if selected_dataframe == options[0]:
        st.write("Users DataFrame:")
        st.write(df_users)


