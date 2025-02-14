import streamlit as st
import math
import pandas as pd
from datetime import datetime

timestamp = datetime.now().strftime("%d-%m-%y")

st.set_page_config(page_title="Stock Market Calculator", page_icon="📈", layout="centered")

# Title of the app
# st.title("Stock Market Calculator")

# Sidebar for navigation
st.sidebar.title("Stock Market Calculator")
st.sidebar.markdown("---")	
calculator_type = st.sidebar.selectbox(
    "Choose a Calculator", ["Position Sizing Calculator", "Market Range Calculator"]
)


# Function to save output to a text file
def save_to_file(filename, content):
    with open(filename, "w") as file:
        file.write(content)
    st.success(f"Output saved to {filename}")


# Position Sizing Calculator
if calculator_type == "Position Sizing Calculator":
    st.header("Position Sizing Calculator")

    # Input fields
    account_size = st.number_input(
        "Account Size ", min_value=0.0, value=10000.0, step=1000.0
    )
    risk_per_trade = st.number_input(
        "Risk per Trade (%)", min_value=0.1, value=1.0, step=0.1
    )
    entry_price = st.number_input("Entry Price ", min_value=0.01, value=50.0, step=1.0)
    stop_loss_price = st.number_input(
        "Stop Loss Price ", min_value=0.01, value=45.0, step=1.0
    )

    # Calculate position size
    if st.button("Calculate Position Size"):
        risk_amount = account_size * (risk_per_trade / 100)
        risk_per_share = entry_price - stop_loss_price
        num_shares = risk_amount / risk_per_share

        # Prepare output for tabular display
        data = {
            "Metric": [
                "Account Size",
                "Risk per Trade",
                "Entry Price",
                "Stop Loss Price",
                "Risk Amount",
                "Number of Shares",
            ],
            "Value": [
                f"{account_size:.2f}",
                f"{risk_per_trade}%",
                f"{entry_price:.2f}",
                f"{stop_loss_price:.2f}",
                f"{risk_amount:.2f}",
                f"{math.floor(num_shares)}",
            ],
        }
        df = pd.DataFrame(data)

        # Display results in a table
        st.subheader("Results:")
        st.table(df)

        # Prepare output for saving to file
        output = (
            f"Position Sizing Calculator Results\n"
            f"---------------------------------\n"
            f"Account Size: {account_size:.2f}\n"
            f"Risk per Trade: {risk_per_trade}%\n"
            f"Entry Price: {entry_price:.2f}\n"
            f"Stop Loss Price: {stop_loss_price:.2f}\n"
            f"Risk Amount: {risk_amount:.2f}\n"
            f"Number of Shares: {math.floor(num_shares)}\n"
        )

        # Save to file
        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"position_sizing_{timestamp}.txt"
        save_to_file(filename, output)

# Market Range Calculator based on INDIA VIX
elif calculator_type == "Market Range Calculator":
    st.header("Market Range Calculator (Based on INDIA VIX)")

    # Input fields
    current_spot_price = st.number_input(
        "Current Spot Price ", min_value=0.01, value=5000.0, step=10.0
    )
    india_vix = st.number_input("INDIA VIX (%)", min_value=0.1, value=20.0, step=0.1)

    # Calculate market ranges
    if st.button("Calculate Market Range"):
        # Calculate ranges
        annual_range = current_spot_price * (india_vix / 100)
        monthly_range = annual_range / math.sqrt(12)
        weekly_range = annual_range / math.sqrt(52)

        # Calculate upper and lower levels
        annual_upper = current_spot_price + annual_range
        annual_lower = current_spot_price - annual_range
        monthly_upper = current_spot_price + monthly_range
        monthly_lower = current_spot_price - monthly_range
        weekly_upper = current_spot_price + weekly_range
        weekly_lower = current_spot_price - weekly_range

        # Create a DataFrame for tabular display
        data = {
            "Range": ["Annual", "Monthly", "Weekly"],
            "Upper Level": [f"{annual_upper:.2f}", f"{monthly_upper:.2f}", f"{weekly_upper:.2f}"],
            "Lower Level": [f"{annual_lower:.2f}", f"{monthly_lower:.2f}", f"{weekly_lower:.2f}"],
        }
        df = pd.DataFrame(data)
        print(df)

        # Display results in a table
        st.subheader("Results:")
        st.table(df)

        # Prepare output for saving to file
        output = (
            f"Market Range Calculator Results\n"
            f"------------------------------\n"
            f"Current Spot Price: {current_spot_price:.2f}\n"
            f"INDIA VIX: {india_vix}%\n\n"
            f"Annual Range:\n"
            f"  Upper Level: {annual_upper:.2f}\n"
            f"  Lower Level: {annual_lower:.2f}\n\n"
            f"Monthly Range:\n"
            f"  Upper Level: {monthly_upper:.2f}\n"
            f"  Lower Level: {monthly_lower:.2f}\n\n"
            f"Weekly Range:\n"
            f"  Upper Level: {weekly_upper:.2f}\n"
            f"  Lower Level: {weekly_lower:.2f}\n"
        )

        # Save to file
        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"market_range_{timestamp}.txt"
        save_to_file(filename, output)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Created with ❤️ by BT")
