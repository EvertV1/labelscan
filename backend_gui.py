import pandas as pd
import streamlit as st
import api_client_online as api_client
import welcome_page


####################################################
# backend gui
####################################################
def initialize_session_variables():
    if 'accepted_to_database' not in st.session_state:
        st.session_state.accepted_to_database = False

    if 'manager_name' not in st.session_state:
        st.session_state.manager_name = None

    if 'manager_password' not in st.session_state:
        st.session_state.manager_password = None

    if 'selected_dataframe' not in st.session_state:
        st.session_state.selected_dataframe = "user_dataframe"




def app():
    st.title("Backend Data Display")
    if not st.session_state.accepted_to_database:
        welcome_page.Welcome_page()
    else:

        # Add new user to the Users DataFrame
        st.subheader("Add New User")

        with st.form(key='user_form'):
            user_name = st.text_input("User Name")
            user_phone = st.text_input("Phone Number")
            submit_button = st.form_submit_button(label='Add User')

            # Submit the new user to the user dataframe
            if submit_button:
                if not user_name or not user_phone:
                    st.error("Please enter both user name and phone number.")
                else:
                    # Send new user data to FastAPI
                    response = api_client.send_user_to_fastapi(user_name, user_phone)
                    if response:
                        st.success(response.get("message", "User added successfully"))

        # Remove existing user from the Users DataFrame
        st.subheader("Remove Existing User")

        # Fetch user data from FastAPI to get the list of users
        user_list = api_client.users_data_to_select_removal()

        with st.form(key='remove_user_form'):
            user_to_remove = st.selectbox("Select User to Remove", user_list)
            remove_button = st.form_submit_button(label='Remove User')

            # Submit the user to be removed
            if remove_button:
                # Send remove user request to FastAPI
                response = api_client.remove_user_from_database(user_to_remove)
                if response:
                    st.success(response.get("message", "User removed successfully"))
                st.experimental_rerun()

        # Add section to send WhatsApp message
        st.subheader("Send WhatsApp Template")

        with st.form(key='whatsapp_form'):
            user_to_message = st.selectbox("Select User to Message", user_list)
            send_button = st.form_submit_button(label='Send Message')

            # Send WhatsApp message
            if send_button:
                if not user_to_message:
                    st.error("Please select a user")
                else:
                    # Send WhatsApp message to the user
                    response = api_client.send_whatsapp_message(user_to_message)
                    if response:
                        st.success(response.get("message", "WhatsApp message sent successfully"))

        st.subheader("Display of dataframe")
        # Options of different dataframes to show
        options = ['user_dataframe', 'products_dataframe', 'models_dataframe']
        st.session_state.selected_dataframe = st.selectbox('Choose an option', options)

        # Add a button to manually check for new data
        if st.button('Check for New Data'):
            st.experimental_rerun()

        if st.session_state.selected_dataframe == options[1]:
            # Fetch product data from FastAPI and set it in a pandas dataframe
            df_product = api_client.fetch_product_data()

            # Convert the 'product_image' and 'receipt_image' columns to clickable links
            if 'product_image_download' in df_product.columns:
                df_product['product_image_download'] = df_product['product_image_download'].apply(
                    lambda x: f'<a href="{x}" target="_blank">View Image</a>')

            if 'receipt_image_download' in df_product.columns:
                df_product['receipt_image_download'] = df_product['receipt_image_download'].apply(
                    lambda x: f'<a href="{x}" target="_blank">View Receipt</a>')

            # Display the updated DataFrames with clickable links and centered headers
            st.write("Products DataFrame:")
            st.write(df_product.to_html(escape=False, index=False), unsafe_allow_html=True)

        if st.session_state.selected_dataframe == options[2]:
            # Fetch models data from FastAPI and set it in a pandas dataframe
            df_models = api_client.fetch_model_data()

            # Display the updated dataframe
            st.write("Models Dataframe:")
            st.write(df_models)

        if st.session_state.selected_dataframe == options[0]:
            # Fetch models data from FastAPI and set it in a pandas dataframe
            df_users = api_client.fetch_user_data()
            # Display the updated dataframe
            st.write("Users DataFrame:")
            st.write(df_users)

if __name__ == "__main__":
    initialize_session_variables()
    app()

