import streamlit as st
import numpy as np
import plotly.graph_objects as go

from bond_pricing import (
    bond_price, bond_ytm, macaulay_duration, modified_duration,
    convexity, portfolio_duration, immunization_weights
)
from yield_curve import bootstrap_spot_rates

st.set_page_config(page_title="Fixed Income Pricing & Risk", page_icon="💵", layout="wide")

st.title("💵 Fixed Income Pricing & Risk")
st.markdown("Bond pricing, duration, convexity and yield curve bootstrapping.")

st.sidebar.header("⚙️ Bond Parameters")
F = st.sidebar.slider("Face value", 50, 500, 100)
c = st.sidebar.slider("Coupon rate", 0.0, 0.15, 0.05)
T = st.sidebar.slider("Maturity (years)", 1, 30, 5)
y = st.sidebar.slider("Yield", 0.0, 0.15, 0.05)

tab1, tab2, tab3 = st.tabs(["📐 Pricing & Risk", "📈 Yield Curve", "🛡️ Immunization"])

with tab1:
    col_metrics, col_chart = st.columns([1, 2])

    price = bond_price(F, c, T, y)
    mac_dur = macaulay_duration(F, c, T, y)
    mod_dur = modified_duration(F, c, T, y)
    conv = convexity(F, c, T, y)

    with col_metrics:
        st.metric("Bond Price", f"{price:.2f} €")
        st.metric("Macaulay Duration", f"{mac_dur:.2f} yrs")
        st.metric("Modified Duration", f"{mod_dur:.2f}")
        st.metric("Convexity", f"{conv:.2f}")

    with col_chart:
        y_range = np.linspace(0.001, 0.15, 100)
        price_range = [bond_price(F, c, T, yr) for yr in y_range]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=y_range * 100, y=price_range, mode='lines', name='Price',
            line=dict(color="#4DA3FF", width=3),
        ))
        fig.add_vline(x=y * 100, line_dash="dash", line_color="#8FA3BF", annotation_text="Current yield")
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0B1F3A",
            plot_bgcolor="#0B1F3A",
            xaxis_title="Yield (%)",
            yaxis_title="Bond price (€)",
            title="Price vs Yield curve",
            height=500,
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Bootstrap a spot rate curve")
    st.markdown("Using 3 example market bonds (editable in code):")

    bonds = [
        {"maturity": 1, "coupon_rate": 0.0, "price": 96.15, "face_value": 100},
        {"maturity": 2, "coupon_rate": 0.06, "price": 100.50, "face_value": 100},
        {"maturity": 3, "coupon_rate": 0.05, "price": 97.80, "face_value": 100},
    ]

    rates = bootstrap_spot_rates(bonds)
    maturities = [b["maturity"] for b in bonds]

    fig_curve = go.Figure()
    fig_curve.add_trace(go.Scatter(
        x=maturities, y=[r * 100 for r in rates], mode='lines+markers',
        line=dict(color="#7CE38B", width=3), marker=dict(size=10),
    ))
    fig_curve.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0B1F3A",
        plot_bgcolor="#0B1F3A",
        xaxis_title="Maturity (years)",
        yaxis_title="Spot rate (%)",
        title="Bootstrapped Spot Rate Curve",
        height=450,
    )
    st.plotly_chart(fig_curve, use_container_width=True)

with tab3:
    st.subheader("Portfolio immunization")

    target = st.slider("Target horizon (years)", 1, 20, 7)
    d_short = st.slider("Short bond duration", 1, 10, 5)
    d_long = st.slider("Long bond duration", 5, 30, 10)

    if d_short < d_long:
        w_short, w_long = immunization_weights(target, d_short, d_long)
        port_dur = portfolio_duration([w_short, w_long], [d_short, d_long])

        col1, col2, col3 = st.columns(3)
        col1.metric("Weight short bond", f"{w_short*100:.1f}%")
        col2.metric("Weight long bond", f"{w_long*100:.1f}%")
        col3.metric("Portfolio duration", f"{port_dur:.2f} yrs")
    else:
        st.warning("Short bond duration must be less than long bond duration.")