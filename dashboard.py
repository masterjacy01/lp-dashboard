import pandas as pd
import streamlit as st
import requests
import plotly.graph_objects as go

# Access the API endpoints from st.secrets
API_ENDPOINT_1 = st.secrets["api_endpoints"]["endpoint_1"]
API_ENDPOINT_2 = st.secrets["api_endpoints"]["endpoint_2"]
API_ENDPOINT_3 = st.secrets["api_endpoints"]["endpoint_3"]
API_ENDPOINT_4 = st.secrets["api_endpoints"]["endpoint_4"]

@st.cache_data(ttl=300)  # Cache results for 5 minutes (300 seconds)
def fetch_data(api_endpoint):
    """Fetch data from the API endpoint."""
    try:
        response = requests.get(api_endpoint)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred while fetching data from {api_endpoint}: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        st.error(f"Connection error occurred while fetching data from {api_endpoint}: {conn_err}")
    except Exception as e:
        st.error(f"An error occurred while fetching data from {api_endpoint}: {e}")
    return {}


def display_vault_data(data):
    """Display the vault data."""
    st.subheader("Vault Data")
    st.write("Vault Address:", data["vaultAddress"])
    st.write("Token 0 Address:", data["token0Address"])
    st.write("Token 0 Decimals:", data["token0Decimals"])
    st.write("Token 0 Symbol:", data["token0Symbol"])
    st.write("Token 1 Address:", data["token1Address"])
    st.write("Token 1 Decimals:", data["token1Decimals"])
    st.write("Token 1 Symbol:", data["token1Symbol"])

def display_liquidity_overview(data):
    """Display liquidity overview."""
    st.subheader("Liquidity Overview")
    st.write("Sum Token 0:", data["sumToken0"])
    st.write("Sum Token 1:", data["sumToken1"])
    st.write("Liquidity 0:", data["liquidity0"])
    st.write("Liquidity 1:", data["liquidity1"])
    st.write("Unclaimed Fee 0:", data["unclaimedfee0"])
    st.write("Unclaimed Fee 1:", data["unclaimedfee1"])
    st.write("Leftover 0:", data["leftover0"])
    st.write("Leftover 1:", data["leftover1"])

def display_liquidity_positions(data):
    """Display liquidity positions."""
    st.subheader("Liquidity Positions")
    
    # Extract positions data
    positions = data["positions"]
    
    # Extract and round lower and upper prices for the bars
    lower_prices = [round(pos["range"]["lowerPrice"], 2) for pos in positions]
    upper_prices = [round(pos["range"]["upperPrice"], 2) for pos in positions]
    range_lengths = [upper - lower for upper, lower in zip(upper_prices, lower_prices)]
    names = [f"Position {i+1}" for i in range(len(positions))]
    
    # Prepare hover text with rounded values
    hover_text = [
        f"Range: {lower} - {upper}<br>Amount 0: {pos['amount0']}<br>Amount 1: {pos['amount1']}"
        for pos, lower, upper in zip(positions, lower_prices, upper_prices)
    ]

    # Create the bar chart using plotly
    fig = go.Figure(go.Bar(
        x=range_lengths,
        y=names,
        orientation='h',
        base=lower_prices,
        text=hover_text,
        hoverinfo="text"
    ))
    fig.update_layout(title="Open Ranges", xaxis_title="Price")
    
    st.plotly_chart(fig)
    
    # Display detailed information
    for pos, lower, upper in zip(positions, lower_prices, upper_prices):
        st.write(f"Range: {lower} - {upper}")
        st.write("Amount 0:", pos["amount0"])
        st.write("Amount 1:", pos["amount1"])
        st.write("---")

def display_data_for_endpoint(api_endpoint):
    """Display data for a given API endpoint."""
    
    # Fetch the data
    data = fetch_data(api_endpoint)
    
    # Display the data in a structured manner
    if "liquidityOverview" in data:
        display_liquidity_overview(data["liquidityOverview"])
    if "liquidityPositions" in data:
        display_liquidity_positions(data["liquidityPositions"])
    if "vaultData" in data:
        display_vault_data(data["vaultData"])

def main():
    """Main function for the Streamlit app."""
    st.title("Brokkr LP Vaults Current State")
    
    # Create tabs for each API endpoint
    tab1, tab2, tab3, tab4 = st.tabs(["Bullish", "Bearish", "Hodl", "Block"])

    with tab1:
        display_data_for_endpoint(API_ENDPOINT_1)

    with tab2:
        display_data_for_endpoint(API_ENDPOINT_2)

    with tab3:
        display_data_for_endpoint(API_ENDPOINT_3)

    with tab4:
        display_data_for_endpoint(API_ENDPOINT_4)

if __name__ == "__main__":
    main()
