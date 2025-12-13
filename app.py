import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# Page configuration
# -------------------------------
st.set_page_config(page_title="AI Business Decision Simulator", layout="wide")

st.title("📊 AI Business Decision Simulator")
st.write("End-to-end business analytics, risk modeling & strategic decision system")

# -------------------------------
# Load data
# -------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("synthetic_business_data.csv")

df = load_data()

# -------------------------------
# Show raw data
# -------------------------------
st.subheader("📂 Business Dataset")
st.dataframe(df.head())

# -------------------------------
# Key Metrics
# -------------------------------
st.subheader("📌 Key Business Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Average Profit", f"{df['Profit'].mean():,.2f}")
col2.metric("Average Revenue", f"{df['Revenue'].mean():,.2f}")
col3.metric("Average Current Ratio", f"{df['Current_Ratio'].mean():.2f}")

# -------------------------------
# Monte Carlo Simulation
# -------------------------------
st.subheader("🎲 Monte Carlo Risk Simulation")

avg_price = df["Price"].mean()
avg_units = df["Units_Sold"].mean()
avg_cost = df["Total_Cost"].mean()

units_std = df["Units_Sold"].std()
cost_std = df["Total_Cost"].std()

np.random.seed(42)
simulated_profits = []

for _ in range(1000):
    units = max(np.random.normal(avg_units, units_std), 0)
    cost = max(np.random.normal(avg_cost, cost_std), 0)
    revenue = avg_price * units
    simulated_profits.append(revenue - cost)

simulated_profits = np.array(simulated_profits)

expected_profit = simulated_profits.mean()
loss_prob = (simulated_profits < 0).mean() * 100
VaR_95 = np.percentile(simulated_profits, 5)

st.write("**Expected Profit:**", round(expected_profit, 2))
st.write("**Loss Probability (%):**", round(loss_prob, 2))
st.write("**Value at Risk (95%):**", round(VaR_95, 2))

# -------------------------------
# Profit Distribution Chart
# -------------------------------
fig, ax = plt.subplots()
ax.hist(simulated_profits, bins=40)
ax.axvline(expected_profit, linestyle="--", label="Expected Profit")
ax.axvline(VaR_95, linestyle="--", label="VaR 95%")
ax.legend()
ax.set_title("Profit Distribution (Monte Carlo Simulation)")
st.pyplot(fig)

# -------------------------------
# Final Recommendation
# -------------------------------
st.subheader("🧠 Strategic Recommendation")

latest = df.iloc[-1]

if latest["Profit"] > expected_profit and latest["Current_Ratio"] >= 1.5:
    decision = "🚀 AGGRESSIVE EXPANSION"
elif latest["Current_Ratio"] < 1:
    decision = "⚠️ COST CUTTING REQUIRED"
else:
    decision = "🟡 CONTROLLED GROWTH"

st.success(f"**Final Decision:** {decision}")
