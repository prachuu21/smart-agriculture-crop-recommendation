import streamlit as st
import pandas as pd
import pickle
import os
import base64

# -----------------------------
# Load trained model
# -----------------------------
with open("crop_model.pkl", "rb") as file:
    model = pickle.load(file)

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Smart Agriculture",
    page_icon="🌱",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 600;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .result-box {
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    border: 1px solid #c8ddcc;
    margin-top: 30px;
    margin-bottom: 20px;

    background: linear-gradient(
        135deg,
         #e8f5e9 0%,
        #d5ead8 50%,
        #c4e1c8 100%
    );

    box-shadow:  0 8px 20px rgba(40, 100, 50, 0.12) ;
}

.result-box::before {
    content: "🌿";
    position: absolute;
    left: 18px;
    top: 12px;
    font-size: 42px;
    transform: rotate(-15deg);
}

.result-box::after {
    content: "🌾";
    position: absolute;
    right: 18px;
    bottom: 8px;
    font-size: 48px;
    transform: rotate(12deg);
}

.result-title {
    font-size: 21px;
    font-weight: 800;
    color: #173d24;
    margin-bottom: 10px;
}

.crop-icon {
    font-size: 42px;
    margin: 5px 0;
}

.crop-name {
    font-size: 44px;
    font-weight: 800;
    color: #123b20;
    margin-top: 8px 0 12px 0;
}

.result-description {
    font-size: 16px;
    color: #36533d
    margin-top: 8px;
}

.graphic-row {
    font-size: 25px;
    margin-top: 15px;
    letter-spacing: 8px;
}
.header-banner {
    background-image: url("header_agriculutre.jpeg");
    background-size: cover;
    background-position: center;
    padding: 60px 30px;
    border-radious: 15px;
}
.header-content{
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Header
# -----------------------------
with open("header_agriculture.jpeg", "rb") as image_file:
    image_base64 = base64.b64encode(image_file.read()).decode()

st.markdown(
    f"""
    <div class="header-banner">
        <img src="data:image/jpeg;base64,{image_base64}"
             style="width:100%; height:180px; object-fit:cover; border-radius:15px;">
        <div class="header-content">
            <h1>🌱 Smart Agriculture</h1>
            <p>AI-Based Crop Recommendation System</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

 

st.write(
    "Enter the soil and weather conditions to get a suitable crop recommendation."
)

st.divider()

# -----------------------------
# Input sections
# -----------------------------
col1, col2 = st.columns(2)

# Soil parameters
with col1:
    st.markdown(
        '<div class="section-title">🧪 Soil Parameters</div>',
        unsafe_allow_html=True
    )

    N = st.number_input(
        "Nitrogen (N)",
        min_value=0.0,
        value=50.0
    )

    P = st.number_input(
        "Phosphorus (P)",
        min_value=0.0,
        value=50.0
    )

    K = st.number_input(
        "Potassium (K)",
        min_value=0.0,
        value=50.0
    )

    ph = st.number_input(
        "Soil pH",
        min_value=0.0,
        max_value=14.0,
        value=6.5
    )

# Weather parameters
with col2:
    st.markdown(
        '<div class="section-title">🌦️ Weather Parameters</div>',
        unsafe_allow_html=True
    )

    temperature = st.number_input(
        "Temperature (°C)",
        value=25.0
    )

    humidity = st.number_input(
        "Humidity (%)",
        min_value=0.0,
        max_value=100.0,
        value=60.0
    )

    rainfall = st.number_input(
        "Rainfall (mm)",
        min_value=0.0,
        value=100.0
    )

st.divider()

# -----------------------------
# Buttons
# -----------------------------
button_col1, button_col2, button_col3 = st.columns([1, 2, 1])

with button_col2:
    recommend = st.button(
        "🌾 Recommend Crop",
        use_container_width=True
    )

    reset = st.button(
        "🔄 Reset",
        use_container_width=True
    )

# Reset inputs
if reset:
    st.rerun()

# -----------------------------
# Prediction
# -----------------------------
if recommend:

    input_data = pd.DataFrame(
        [[N, P, K, temperature, humidity, ph, rainfall]],
        columns=[
            "N",
            "P",
            "K",
            "temperature",
            "humidity",
            "ph",
            "rainfall"
        ]
    )

    prediction = model.predict(input_data)

    crop = prediction[0]

     

    st.markdown(
    f"""<div style="background: linear-gradient(135deg, #dff7e3, #b8f2c2); padding: 25px; border-radius: 18px; border: 2px solid #52b788; box-shadow: 0 6px 18px rgba(0,0,0,0.12); text-align: center; margin: 20px 0;">
<div style="font-size: 22px; font-weight: 700; color: #1b5e20;">
🌱 The Recommended Crop
</div>
<div style="font-size: 38px; font-weight: 800; color: #14532d; margin: 10px 0;">
{crop.title()}
</div>
<div style="display: inline-block; background: white; padding: 8px 18px; border-radius: 20px; color: #166534; font-weight: 600;">
✅ Best suited for your current conditions
</div>
</div>""",
    unsafe_allow_html=True
)
# Input Summary
st.markdown("### 📊 Input Summary")

summary_col1, summary_col2 = st.columns(2)

with summary_col1:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #d9f99d, #86efac);
        padding: 18px;
        border-radius: 15px;
        margin-bottom: 12px;
        color: #14532d;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    ">
        <h4>🌱 Nitrogen (N)</h4>
        <h2>{N:.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #fde68a, #fbbf24);
        padding: 18px;
        border-radius: 15px;
        margin-bottom: 12px;
        color: #78350f;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    ">
        <h4>💧 Humidity</h4>
        <h2>{humidity:.2f}%</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #bae6fd, #60a5fa);
        padding: 18px;
        border-radius: 15px;
        color: #1e3a8a;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    ">
        <h4>🌧️ Rainfall</h4>
        <h2>{rainfall:.2f} mm</h2>
    </div>
    """, unsafe_allow_html=True)


with summary_col2:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #ddd6fe, #a78bfa);
        padding: 18px;
        border-radius: 15px;
        margin-bottom: 12px;
        color: #4c1d95;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    ">
        <h4>🧪 Phosphorus (P)</h4>
        <h2>{P:.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #fed7aa, #fb923c);
        padding: 18px;
        border-radius: 15px;
        margin-bottom: 12px;
        color: #7c2d12;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    ">
        <h4>🌡️ Temperature</h4>
        <h2>{temperature:.2f} °C</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #fbcfe8, #f472b6);
        padding: 18px;
        border-radius: 15px;
        color: #831843;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    ">
        <h4>⚗️ Soil pH</h4>
        <h2>{ph:.2f}</h2>
    </div>
    """, unsafe_allow_html=True)
# -----------------------------
# Footer
# -----------------------------
st.divider()

st.caption(
    "Smart Agriculture | AI-based Crop Recommendation System"
)