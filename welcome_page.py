import streamlit as st
import time
import api_client

def Welcome_page():
    # Welcome page with terms and conditions
    st.title("Welcome to the App!")



    # Show input fields for user details once terms are accepted
    st.subheader("Please enter your credentials for access to the database:")
    st.session_state.manager_name = st.text_input("Name")
    st.session_state.manager_password = st.text_input("Password")

    # Button to submit the user details
    if st.button("Submit Details"):
        # Ensure both fields are filled out
        if st.session_state.manager_name and st.session_state.manager_password:
            # Check if the user exists in the system
            user_exists = api_client.check_manager(st.session_state.manager_name, st.session_state.manager_password)
            if user_exists:
                st.success("Details submitted successfully, you are approved!")
                # Wait for 2 seconds before processing the response
                time.sleep(2)
                # Set the session state to move to the next page
                st.session_state.accepted_to_database = True
                st.experimental_rerun()  # Refresh the app to navigate to the next page
            else:
                st.write("Sorry, it appears that you do not currently have access to this application. "
                         "Please contact your manager to obtain the necessary permissions.")
        else:
            # Show an error if fields are incomplete
            st.error("Please fill in both fields.")

    # # Debugging: Check the session state variables
    # st.write("Session state variables:")
    # st.write(st.session_state)