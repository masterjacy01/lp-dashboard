import pandas as pd
import streamlit as st
import requests
import plotly.graph_objects as go

# Define the API endpoint
API_ENDPOINT = "http://206.189.56.114/metrics/status"

@st.cache_data(ttl=300)  # Cache results for 5 minutes (300 seconds)
def fetch_data():
    """Fetch data from the API endpoint."""
    response = requests.get(API_ENDPOINT)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data from the API.")
        return {}

def display_vault_data(data):
    """Display the vault data."""
    st.subheader("Vault Data")
    st.write("Vault Address:", data["vaultAddress"])
    st.write("Fee Tier:", data["feeTier"])
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
    
    # Extract lower and upper prices for the bars
    lower_prices = [pos["range"]["lowerPrice"] for pos in positions]
    range_lengths = [pos["range"]["upperPrice"] - pos["range"]["lowerPrice"] for pos in positions]
    names = [f"Position {i+1}" for i in range(len(positions))]

    # Create the bar chart using plotly
    fig = go.Figure(go.Bar(
        x=range_lengths,
        y=names,
        orientation='h',
        base=lower_prices,
        text=positions,
        hoverinfo="text"
    ))
    fig.update_layout(title="Open Ranges", xaxis_title="Price")
    
    st.plotly_chart(fig)
    
    for position in positions:
        st.write("Range:", f"{position['range']['lowerPrice']} - {position['range']['upperPrice']}")
        st.write("Amount 0:", position["amount0"])
        st.write("Amount 1:", position["amount1"])
        st.write("---")

def main():
    """Main function for the Streamlit app."""
    st.title("HODL & LP Strategy Current State")
    
    # Fetch the data
    data = fetch_data()
    
    # Display the data in a structured manner
    if "liquidityOverview" in data:
        display_liquidity_overview(data["liquidityOverview"])
    if "liquidityPositions" in data:
        display_liquidity_positions(data["liquidityPositions"])
    if "vaultData" in data:
        display_vault_data(data["vaultData"])

if __name__ == "__main__":
    main()
