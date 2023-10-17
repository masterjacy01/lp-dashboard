import streamlit as st
import requests

# Define the API endpoint
API_ENDPOINT = "http://206.189.56.114/metrics/status"

def fetch_data():
    """Fetch data from the API endpoint."""
    response = requests.get(API_ENDPOINT)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data from the API.")
        return {}

def main():
    """Main function for the Streamlit app."""
    st.title("API Data Visualization")
    
    # Fetch the data
    data = fetch_data()
    
    # Check if data is not empty
    if data:
        st.write(data)  # Display raw data for now. You can modify this to create plots/visualizations.
        
        # Example visualization (you can customize this based on the data structure):
        # st.bar_chart(data['some_key'])

if __name__ == "__main__":
    main()
