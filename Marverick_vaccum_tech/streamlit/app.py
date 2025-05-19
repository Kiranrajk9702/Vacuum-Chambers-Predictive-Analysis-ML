import streamlit as st
import pickle
import pandas as pd
import shap
import matplotlib.pyplot as plt
from PIL import Image

# ✅ Load the saved ML model
with open(r"streamlit/vaccum_chamber_maintenance_ML.pkl", "rb") as f:
    model = pickle.load(f)

# ✅ Page Configuration
st.set_page_config(page_title="Predictive Maintenance Dashboard", page_icon="🔧", layout="wide")

# ✅ Sidebar Navigation
st.sidebar.header("Navigation")
selected_option = st.sidebar.radio("Choose an option:", ["📂 Upload Data", "📊 View Dashboard"])

# ✅ Upload file globally for accessibility across all sections
uploaded_file = st.file_uploader("📂 Upload Sensor Data (CSV)", type=["csv"])

# ✅ Show Dashboard when selected in sidebar
if selected_option == "📊 View Dashboard":
    image = Image.open("streamlit/Dashboard.png")  # Replace with your PNG filename
    st.image(image, caption="📊 Power BI Dashboard", use_container_width=True)

# ✅ Upload & Predict Section
if selected_option == "📂 Upload Data" and uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Ensure the input data matches the training features
    expected_features = ["Type", "Air temperature [K]", "Process temperature [K]", "Rotational speed [rpm]", 
                         "Torque [Nm]", "Tool wear [min]", "Target", "Torque_Speed_Ratio", "Wear_Temperature_Ratio"]

    # Drop columns not in expected features
    extra_columns = [col for col in df.columns if col not in expected_features]
    if extra_columns:
        df = df.drop(columns=extra_columns)

    # Encode the 'Type' column into numeric values if it exists
    if 'Type' in df.columns:
        df['Type'] = df['Type'].astype('category').cat.codes

    # Reorder columns to match the training data
    missing_features = [col for col in expected_features if col not in df.columns]
    if missing_features:
        st.error(f"❌ Missing required columns: {missing_features}")
    else:
        df = df[expected_features]

        # Show data preview
        st.markdown("### 🔍 Data Preview")
        st.dataframe(df.head())

        # Make predictions
        predictions = model.predict(df)
        df["Failure Prediction"] = predictions

        # Map numeric predictions to meaningful failure types
        failure_mapping = {
            0: "✅ No Failure",
            1: "⚠️ Minor Issue",
            2: "🔶 Warning",
            3: "🔥 Critical Failure"
        }
        df["Failure Type Predicted"] = df["Failure Prediction"].map(failure_mapping)

        st.markdown("### 📊 Prediction Results")
        st.dataframe(df)

        # Download results
        csv = df.to_csv(index=False).encode()
        st.download_button(label="⬇️ Download Predictions as CSV", data=csv, file_name="predictions.csv", mime="text/csv")

# ✅ SHAP Explainability Section
if selected_option == "🔍 Explainability (SHAP)" and uploaded_file is not None:
    st.subheader("🔍 SHAP Explainability - Feature Impact")

    # Load Data
    df = pd.read_csv(uploaded_file)

    # Generate SHAP explanations
    explainer = shap.TreeExplainer(model)  # Adjust based on your model type
    shap_values = explainer.shap_values(df)

    # Interactive Force Plot (only works in Jupyter but embedded as HTML in Streamlit)
    st.markdown("### 🔬 SHAP Force Plot (First Sample)")
    shap.initjs()
    force_plot_html = shap.force_plot(explainer.expected_value, shap_values[0, :], df.iloc[0, :], matplotlib=False)
    st.components.v1.html(force_plot_html, height=400)  # Embed in Streamlit

    # Summary Plot - Feature Importance
    st.markdown("### 📊 Feature Importance")
    fig, ax = plt.subplots()
    shap.summary_plot(shap_values, df, show=False)
    st.pyplot(fig)

elif selected_option == "🔍 Explainability (SHAP)":
    st.warning("📂 Please upload sensor data to view SHAP explanations.")

# ✅ Footer
st.markdown("---")
st.markdown("💡 Need help? Check out the **Documentation** or Contact Support.")

