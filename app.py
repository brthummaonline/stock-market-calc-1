import streamlit as st
import math
import pandas as pd
from datetime import datetime
from scipy.stats import norm

timestamp = datetime.now().strftime("%d-%m-%y")

# Helper function to format numbers
def format_number(value):
    return f"{int(value)}" if value == int(value) else f"{value:.2f}"

st.set_page_config(page_title="Stock Market Calculator", page_icon="📈", layout="centered")

# Title of the app
# st.title("Stock Market Calculator")

# Sidebar for navigation
st.sidebar.title("Stock Market Calculator")
st.sidebar.markdown("---")	
calculator_type = st.sidebar.selectbox(
    "Choose a Calculator", ["Position Sizing Calculator", "Market Range Calculator","Options Probability Calculator"]
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
# Options Strike Level Expiry Probability Calculator
elif calculator_type == "Options Probability Calculator":
    st.header("Options Strike Level Expiry Probability Calculator")
    
    # Input fields
    current_stock_price = st.number_input("Current Stock Price ($)", min_value=0.01, value=25000.0, step=10.0)
    call_implied_vol = st.number_input("Call Implied Volatility (%)", min_value=0.01, value=16.22, step=0.01)
    put_implied_vol = st.number_input("Put Implied Volatility (%)", min_value=0.01, value=20.54, step=0.01)
    days_to_expiration = st.number_input("Days to Expiration", min_value=1, value=2, step=1)
    call_target_price = st.number_input("Call Target Price ($)", min_value=0.01, value=25200.0, step=10.0)
    put_target_price = st.number_input("Put Target Price ($)", min_value=0.01, value=24800.0, step=10.0)
    
    # Calculate probabilities
    if st.button("Calculate Probabilities"):
        # Convert implied volatilities to decimals
        call_vol = call_implied_vol / 100
        put_vol = put_implied_vol / 100
        
        # Calculate call probability
        call_distance = call_target_price - current_stock_price
        call_d1 = (math.log(current_stock_price / call_target_price) + (0.5 * call_vol**2 * days_to_expiration / 365))
        call_d1 /= (call_vol * math.sqrt(days_to_expiration / 365))
        call_prob = norm.cdf(call_d1)
        
        # Calculate put probability
        put_distance = current_stock_price - put_target_price
        put_d1 = (math.log(current_stock_price / put_target_price) - (0.5 * put_vol**2 * days_to_expiration / 365))
        put_d1 /= (put_vol * math.sqrt(days_to_expiration / 365))
        put_prob = norm.cdf(-put_d1)
        
        # # Calculate probability of expiring in range
        # range_prob = norm.cdf(call_d1) - norm.cdf(put_d1)  # Corrected formula
        
        # # Ensure non-negative probability
        # range_prob = max(range_prob, 0)  # Prevent negative probabilities
        
        # Prepare output for tabular display
        call_data = {
            "Target": ["Call"],
            "Strike Price": [f"${int(call_target_price)}"],  # Display as integer
            "Winning Probability": [f"{call_prob * 100:.2f}%"],
            "Close Above Target": [f"{format_number(call_distance)}"],
        }
        put_data = {
            "Target": ["Put"],
            "Strike Price": [f"${int(put_target_price)}"],  # Display as integer
            "Winning Probability": [f"{put_prob * 100:.2f}%"],
            "Close Below Target": [f"{format_number(put_distance)}"],
        }
        # range_data = {
        #     "Probability of Expiring in Range": [f"{range_prob * 100:.2f}%"],
        #     "Lower Level": [f"${int(put_target_price)}"],  # Display as integer
        #     "Upper Level": [f"${int(call_target_price)}"],  # Display as integer
        # }
        
        call_df = pd.DataFrame(call_data)
        put_df = pd.DataFrame(put_data)
        # range_df = pd.DataFrame(range_data)
        
        # Display results in tables
        st.subheader("Call Probabilities:")
        st.table(call_df)
        
        st.subheader("Put Probabilities:")
        st.table(put_df)
        
        # st.subheader("Probability of Expiring in Range:")
        # st.table(range_df)
        
        # Prepare output for saving to file
        output = (
            f"Options Strike Level Expiry Probability Calculator Results\n"
            f"--------------------------------------------------------\n"
            f"Current Stock Price: ${format_number(current_stock_price)}\n"
            f"Call Implied Volatility: {call_implied_vol}%\n"
            f"Put Implied Volatility: {put_implied_vol}%\n"
            f"Days to Expiration: {days_to_expiration}\n\n"
            f"Call Probabilities:\n"
            f"  Strike Price: ${int(call_target_price)}\n"
            f"  Winning Probability: {call_prob * 100:.2f}%\n"
            f"  Close Above Target: {format_number(call_distance)}\n\n"
            f"Put Probabilities:\n"
            f"  Strike Price: ${int(put_target_price)}\n"
            f"  Winning Probability: {put_prob * 100:.2f}%\n"
            f"  Close Below Target: {format_number(put_distance)}\n\n"
            # f"Probability of Expiring in Range: {range_prob * 100:.2f}%\n"
            # f"  Lower Level: ${int(put_target_price)}\n"
            # f"  Upper Level: ${int(call_target_price)}\n"
        )
        
        # Save to file
        filename = f"options_probability_{timestamp}.txt"
        save_to_file(filename, output)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Created with ❤️ by BT")