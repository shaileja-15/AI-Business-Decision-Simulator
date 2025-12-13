import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =====================================
# Page Configuration
# =====================================
st.set_page_config(
    page_title="AI Business Decision Simulator",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🧠 AI Business Decision Simulator")
st.caption("⚡ Strategy • Risk • AI-Driven Outcomes • Boardroom-Ready Decisions")

# =====================================
# Load Data
# =====================================
@st.cache_data
def load_data():
    return pd.read_csv("synthetic_business_data.csv")

df = load_data()

# =====================================
# Sidebar – USER STRATEGIC INPUTS
# =====================================
st.sidebar.header("🎛️ Strategic Control Panel")

price_change = st.sidebar.slider(
    "💰 Price Change (%)",
    -30, 30, 5
) / 100

marketing_boost = st.sidebar.slider(
    "📢 Marketing Spend Impact (%)",
    0, 50, 10
) / 100

economic_shock = st.sidebar.slider(
    "🌍 Economic Shock Factor",
    -0.5, 0.5, 0.0
)

risk_appetite = st.sidebar.selectbox(
    "⚖️ Risk Appetite",
    ["Low", "Medium", "High"]
)

simulation_runs = st.sidebar.selectbox(
    "🎲 Monte Carlo Simulations",
    [1000, 3000, 5000]
)

# =====================================
# Dataset View
# =====================================
st.subheader("📂 Business Dataset Snapshot")
st.dataframe(df.tail())

# =====================================
# Core Metrics
# =====================================
st.subheader("📊 Current Business Health")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Avg Revenue", f"{df['Revenue'].mean():,.0f}")
col2.metric("Avg Profit", f"{df['Profit'].mean():,.0f}")
col3.metric("Profit Margin", f"{df['Profit_Margin'].mean():.2%}")
col4.metric("Current Ratio", f"{df['Current_Ratio'].mean():.2f}")

# =====================================
# AI-STYLE FUTURE SCENARIO ENGINE
# =====================================
st.subheader("🚀 AI-Driven Future Scenario Engine")

base_price = df["Price"].mean()
base_units = df["Units_Sold"].mean()
base_cost = df["Total_Cost"].mean()

# Adjustments
adjusted_price = base_price * (1 + price_change)
adjusted_units = base_units * (1 + marketing_boost + economic_shock)

units_std = df["Units_Sold"].std()
cost_std = df["Total_Cost"].std()

np.random.seed(42)
profits = []

for _ in range(simulation_runs):
    units = max(np.random.normal(adjusted_units, units_std), 0)
    cost = max(np.random.normal(base_cost, cost_std), 0)
    revenue = adjusted_price * units
    profits.append(revenue - cost)

profits = np.array(profits)

# =====================================
# Risk Intelligence Metrics
# =====================================
expected_profit = profits.mean()
worst_case = np.percentile(profits, 1)
best_case = np.percentile(profits, 99)
loss_probability = (profits < 0).mean() * 100
VaR_95 = np.percentile(profits, 5)

# =====================================
# Display AI Metrics
# =====================================
st.subheader("📉 AI Risk & Opportunity Intelligence")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Expected Profit", f"{expected_profit:,.0f}")
c2.metric("Worst Case (1%)", f"{worst_case:,.0f}")
c3.metric("Best Case (99%)", f"{best_case:,.0f}")
c4.metric("Loss Probability", f"{loss_probability:.2f}%")
c5.metric("VaR (95%)", f"{VaR_95:,.0f}")

# =====================================
# Profit Distribution
# =====================================
st.subheader("📊 Future Profit Distribution")

fig, ax = plt.subplots()
ax.hist(profits, bins=50)
ax.axvline(expected_profit, linestyle="--", label="Expected Profit")
ax.axvline(VaR_95, linestyle="--", label="VaR 95%")
ax.set_title("Monte Carlo Profit Distribution")
ax.legend()
st.pyplot(fig)

# =====================================
# AI-LEVEL STRATEGIC VERDICT
# =====================================
st.subheader("🧠 AI Strategic Verdict")

latest = df.iloc[-1]

if expected_profit > latest["Profit"] * 1.3 and loss_probability < 15:
    verdict = "🚀 **HYPER-GROWTH MODE**"
    explanation = "AI predicts strong upside with controlled downside risk. Scale aggressively."
elif loss_probability > 35:
    verdict = "🛑 **DEFENSIVE STRATEGY REQUIRED**"
    explanation = "Downside risk dominates. Preserve cash, reduce exposure."
elif risk_appetite == "High" and best_case > latest["Profit"] * 2:
    verdict = "🔥 **HIGH-RISK, HIGH-REWARD BET**"
    explanation = "Massive upside possible. Suitable only for bold leadership."
else:
    verdict = "🟡 **SMART CONTROLLED EXPANSION**"
    explanation = "Balanced growth with AI-validated safety margins."

st.success(verdict)
st.write(explanation)

# =====================================
# Boardroom-Ready Closing Insight
# =====================================
st.info(
    f"""
    **AI Insight:**  
    With your current strategic inputs, the business has a **{100-loss_probability:.1f}% chance of success**  
    and a **potential upside of {((best_case/abs(worst_case)) if worst_case != 0 else 0):.1f}×** compared to downside.
    
    👉 *This is the kind of intelligence Fortune-500 boards pay millions for.*
    """
)
