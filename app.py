
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score,
    recall_score, f1_score,
    confusion_matrix, classification_report
)

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="CyberShield AI",
    page_icon="🛡️",
    layout="wide"
)

# ==========================================
# ANIMATED CSS
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(-45deg,
        #050816, #0b1730, #10152b, #061c2c);
    background-size: 400% 400%;
    animation: backgroundMove 15s ease infinite;
    color: white;
}

@keyframes backgroundMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

.hero {
    padding: 25px;
    border-radius: 20px;
    background: linear-gradient(
        120deg,
        rgba(0,220,255,.15),
        rgba(40,80,180,.12)
    );
    border: 1px solid rgba(0,220,255,.3);
    text-align: center;
    animation: fadeIn 1s ease;
}

.hero h1 {
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(90deg,#00e5ff,#60a5fa,#a78bfa);
    -webkit-background-clip: text;
    color: transparent;
}

@keyframes fadeIn {
    from {opacity:0; transform:translateY(20px);}
    to {opacity:1; transform:translateY(0);}
}

.card {
    background: rgba(255,255,255,.06);
    border: 1px solid rgba(255,255,255,.12);
    padding: 20px;
    border-radius: 16px;
    transition: .3s ease;
    margin-bottom: 12px;
}

.card:hover {
    transform: translateY(-5px);
    border-color: #00d9ff;
    box-shadow: 0 0 22px rgba(0,217,255,.2);
}

div[data-testid="stMetric"] {
    background: rgba(255,255,255,.07);
    padding: 15px;
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 15px;
}

div.stButton > button {
    background: linear-gradient(90deg,#0891b2,#4f46e5);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    transition: .3s;
}

div.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 20px #0891b2;
    color: white;
}

section[data-testid="stSidebar"] {
    background: #080f20;
}

h1, h2, h3, p, label {
    color: #e5efff;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE
# ==========================================

if "traffic" not in st.session_state:
    st.session_state.traffic = pd.DataFrame()

if "model" not in st.session_state:
    st.session_state.model = None

if "metrics" not in st.session_state:
    st.session_state.metrics = None

if "dataset" not in st.session_state:
    st.session_state.dataset = None

if "labels" not in st.session_state:
    st.session_state.labels = None

if "feature_columns" not in st.session_state:
    st.session_state.feature_columns = None

if "encoder" not in st.session_state:
    st.session_state.encoder = None

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.markdown("# 🛡️ CyberShield AI")
st.sidebar.caption("Intelligent Network Security")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "🏠 Dashboard",
        "🌐 Live Monitor",
        "📁 Dataset Analyzer",
        "🤖 Model Training",
        "🔍 Threat Prediction",
        "📊 Analytics"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("### SYSTEM STATUS")
st.sidebar.success("Application Online")
st.sidebar.info("Live traffic mode: SIMULATED")

# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="hero">
    <h1>🛡️ CYBERSHIELD AI</h1>
    <p>AI-Powered Predictive Network Threat Detection</p>
    <p>Detect • Analyze • Predict • Protect</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# ==========================================
# DASHBOARD
# ==========================================

if page == "🏠 Dashboard":

    st.subheader("⚡ Security Operations Center")

    total = len(st.session_state.traffic)

    attacks = 0
    if total:
        attacks = (
            st.session_state.traffic["Threat"] != "NORMAL"
        ).sum()

    normal = total - attacks

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Network Events", total)
    c2.metric("Detected Threats", attacks)
    c3.metric("Normal Traffic", normal)
    c4.metric(
        "AI Model",
        "Ready" if st.session_state.model else "Not Trained"
    )

    st.write("")

    st.markdown("### 🚀 Security Modules")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
            <h3>🌐 Network Monitoring</h3>
            <p>Monitor simulated network events and identify suspicious activity.</p>
        </div>
        <div class="card">
            <h3>🤖 Machine Learning</h3>
            <p>Train a Random Forest classifier using network traffic datasets.</p>
        </div>
        <div class="card">
            <h3>🔍 Attack Detection</h3>
            <p>Classify network events into normal and malicious categories.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <h3>📊 Security Analytics</h3>
            <p>Analyze threat distribution, model accuracy and attack patterns.</p>
        </div>
        <div class="card">
            <h3>🚨 Threat Intelligence</h3>
            <p>Display risk levels and suspicious traffic alerts.</p>
        </div>
        <div class="card">
            <h3>📁 Dataset Processing</h3>
            <p>Upload and analyze network traffic CSV datasets.</p>
        </div>
        """, unsafe_allow_html=True)

    st.info(
        "Start with Dataset Analyzer to upload network data, "
        "then train your AI model."
    )

# ==========================================
# LIVE NETWORK MONITOR
# ==========================================

elif page == "🌐 Live Monitor":

    st.subheader("🌐 Live Network Traffic Monitor")

    st.warning(
        "DEMO MODE: This module generates synthetic traffic. "
        "It does not capture real network packets."
    )

    col1, col2 = st.columns(2)

    with col1:
        number = st.slider(
            "Number of simulated events",
            5, 100, 20
        )

    with col2:
        speed = st.slider(
            "Refresh interval (seconds)",
            1, 5, 2
        )

    if st.button("▶ Generate Network Traffic"):

        rows = []

        progress = st.progress(0)
        status = st.empty()

        for i in range(number):

            protocol = np.random.choice(
                ["TCP", "UDP", "ICMP"]
            )

            packets = np.random.randint(10, 2000)
            duration = round(np.random.uniform(0.1, 10), 2)
            destination_port = np.random.choice(
                [80, 443, 22, 53, 8080, 3389]
            )

            # Synthetic demo threat rules
            if packets > 1600:
                threat = "DDoS"
                risk = "CRITICAL"

            elif destination_port == 22 and packets > 900:
                threat = "Brute Force"
                risk = "HIGH"

            elif protocol == "ICMP" and packets > 700:
                threat = "Suspicious"
                risk = "MEDIUM"

            else:
                threat = "NORMAL"
                risk = "LOW"

            rows.append({
                "Time": datetime.now().strftime("%H:%M:%S"),
                "Protocol": protocol,
                "Packets": packets,
                "Duration": duration,
                "Destination Port": destination_port,
                "Threat": threat,
                "Risk": risk
            })

            progress.progress((i + 1) / number)
            status.text(f"Analyzing event {i+1}/{number}")

            time.sleep(min(speed / 10, 0.2))

        new_data = pd.DataFrame(rows)

        st.session_state.traffic = pd.concat(
            [st.session_state.traffic, new_data],
            ignore_index=True
        )

        status.success("Traffic simulation completed!")

    if not st.session_state.traffic.empty:

        df = st.session_state.traffic

        st.markdown("### 🚨 Network Event Logs")

        st.dataframe(
            df.tail(100),
            use_container_width=True,
            hide_index=True
        )

        threat_count = df["Threat"].value_counts()

        fig = px.pie(
            values=threat_count.values,
            names=threat_count.index,
            title="Threat Distribution",
            hole=0.5,
            template="plotly_dark"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.download_button(
            "📥 Download Traffic Logs",
            df.to_csv(index=False),
            "network_logs.csv",
            "text/csv"
        )

# ==========================================
# DATASET ANALYZER
# ==========================================

elif page == "📁 Dataset Analyzer":

    st.subheader("📁 Network Dataset Analyzer")

    uploaded = st.file_uploader(
        "Upload Network Traffic CSV",
        type=["csv"]
    )

    if uploaded is not None:

        try:
            df = pd.read_csv(uploaded)

            st.session_state.dataset = df

            st.success("Dataset uploaded successfully!")

            c1, c2, c3 = st.columns(3)

            c1.metric("Total Records", f"{len(df):,}")
            c2.metric("Total Features", len(df.columns))
            c3.metric(
                "Missing Values",
                int(df.isna().sum().sum())
            )

            st.markdown("### Dataset Preview")

            st.dataframe(
                df.head(20),
                use_container_width=True
            )

            st.markdown("### Dataset Information")

            st.write("Columns:", list(df.columns))

            st.markdown("### Statistical Analysis")

            st.dataframe(
                df.describe(include="all").transpose(),
                use_container_width=True
            )

            st.markdown("### Missing Values")

            missing = df.isna().sum()
            missing = missing[missing > 0]

            if len(missing):
                st.dataframe(missing)
            else:
                st.success("No missing values found.")

        except Exception as e:
            st.error(f"Could not read CSV: {e}")

# ==========================================
# MODEL TRAINING
# ==========================================

elif page == "🤖 Model Training":

    st.subheader("🤖 Machine Learning Model Training")

    df = st.session_state.dataset

    if df is None:
        st.warning("Upload a dataset in Dataset Analyzer first.")
        st.stop()

    st.markdown("### Select Training Parameters")

    target = st.selectbox(
        "Select Target / Attack Label Column",
        df.columns
    )

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    features = [
        col for col in numeric_columns
        if col != target
    ]

    if not features:
        st.error("No usable numeric feature columns found.")
        st.stop()

    selected_features = st.multiselect(
        "Select Input Features",
        features,
        default=features[:min(15, len(features))]
    )

    test_size = st.slider(
        "Testing Data Percentage",
        10, 40, 20
    )

    trees = st.slider(
        "Number of Random Forest Trees",
        50, 500, 150, step=50
    )

    if st.button("🚀 Train AI Model", type="primary"):

        try:
            work = df[selected_features + [target]].copy()

            work[target] = work[target].astype(str).str.strip()
            work = work.replace([np.inf, -np.inf], np.nan)
            work = work.dropna(subset=[target])

            X = work[selected_features].apply(
                pd.to_numeric, errors="coerce"
            )

            y_raw = work[target]

            valid = y_raw != ""
            X = X.loc[valid]
            y_raw = y_raw.loc[valid]

            encoder = LabelEncoder()
            y = encoder.fit_transform(y_raw)

            if len(encoder.classes_) < 2:
                st.error("Training requires at least two target classes.")
                st.stop()

            counts = pd.Series(y).value_counts()

            stratify = y if counts.min() >= 2 else None

            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=test_size / 100,
                random_state=42,
                stratify=stratify
            )

            imputer = SimpleImputer(strategy="median")

            X_train = imputer.fit_transform(X_train)
            X_test = imputer.transform(X_test)

            model = RandomForestClassifier(
                n_estimators=trees,
                random_state=42,
                n_jobs=-1,
                class_weight="balanced"
            )

            with st.spinner("Training AI model..."):
                model.fit(X_train, y_train)

                predictions = model.predict(X_test)

            accuracy = accuracy_score(
                y_test, predictions
            )

            precision = precision_score(
                y_test,
                predictions,
                average="weighted",
                zero_division=0
            )

            recall = recall_score(
                y_test,
                predictions,
                average="weighted",
                zero_division=0
            )

            f1 = f1_score(
                y_test,
                predictions,
                average="weighted",
                zero_division=0
            )

            st.session_state.model = model
            st.session_state.imputer = imputer
            st.session_state.encoder = encoder
            st.session_state.feature_columns = selected_features
            st.session_state.metrics = {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1": f1,
                "y_test": y_test,
                "predictions": predictions,
                "report": classification_report(
                    y_test,
                    predictions,
                    target_names=[
                        str(c) for c in encoder.classes_
                    ],
                    zero_division=0
                )
            }

            st.success("AI Model trained successfully!")

            a, b, c, d = st.columns(4)

            a.metric("Accuracy", f"{accuracy*100:.2f}%")
            b.metric("Precision", f"{precision*100:.2f}%")
            c.metric("Recall", f"{recall*100:.2f}%")
            d.metric("F1 Score", f"{f1*100:.2f}%")

            cm = confusion_matrix(
                y_test,
                predictions,
                labels=np.arange(len(encoder.classes_))
            )

            fig = px.imshow(
                cm,
                text_auto=True,
                x=encoder.classes_,
                y=encoder.classes_,
                labels={
                    "x": "Predicted",
                    "y": "Actual",
                    "color": "Count"
                },
                title="Confusion Matrix",
                template="plotly_dark",
                color_continuous_scale="Blues"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.markdown("### Classification Report")

            st.code(
                st.session_state.metrics["report"]
            )

            importance = pd.DataFrame({
                "Feature": selected_features,
                "Importance": model.feature_importances_
            }).sort_values(
                "Importance", ascending=False
            )

            fig = px.bar(
                importance.head(15),
                x="Importance",
                y="Feature",
                orientation="h",
                title="Top Feature Importance",
                template="plotly_dark"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        except Exception as e:
            st.error(f"Training failed: {e}")

# ==========================================
# THREAT PREDICTION
# ==========================================

elif page == "🔍 Threat Prediction":

    st.subheader("🔍 AI Threat Prediction")

    model = st.session_state.model

    if model is None:
        st.warning("Train your model before predicting attacks.")
        st.stop()

    features = st.session_state.feature_columns
    encoder = st.session_state.encoder
    imputer = st.session_state.imputer

    st.markdown("### Enter Network Traffic Features")

    values = {}

    cols = st.columns(2)

    for i, feature in enumerate(features):

        with cols[i % 2]:
            values[feature] = st.number_input(
                feature,
                value=0.0,
                format="%.5f",
                key=f"prediction_{feature}"
            )

    if st.button("🔎 Analyze Network Traffic"):

        input_df = pd.DataFrame(
            [values],
            columns=features
        )

        input_data = imputer.transform(input_df)

        prediction = model.predict(input_data)[0]

        predicted_label = encoder.inverse_transform(
            [prediction]
        )[0]

        probabilities = model.predict_proba(input_data)[0]

        confidence = float(np.max(probabilities)) * 100

        st.markdown("### AI Analysis Result")

        if str(predicted_label).strip().upper() in [
            "BENIGN", "NORMAL", "0"
        ]:
            st.success("🟢 Normal Traffic Detected")
        else:
            st.error("🚨 Potential Threat Detected")

        st.metric("Predicted Class", str(predicted_label))
        st.metric("Model Confidence", f"{confidence:.2f}%")

        probability_df = pd.DataFrame({
            "Attack Type": encoder.classes_,
            "Probability": probabilities
        })

        fig = px.bar(
            probability_df,
            x="Attack Type",
            y="Probability",
            color="Probability",
            title="Prediction Probability",
            template="plotly_dark"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.info(
            "Predictions are model estimates, not proof of an attack. "
            "Verify suspicious traffic before taking action."
        )

# ==========================================
# ANALYTICS
# ==========================================

elif page == "📊 Analytics":

    st.subheader("📊 AI Security Analytics")

    metrics = st.session_state.metrics

    if metrics is None:
        st.warning("Train a model to view analytics.")
        st.stop()

    metric_df = pd.DataFrame({
        "Metric": [
            "Accuracy", "Precision", "Recall", "F1 Score"
        ],
        "Score": [
            metrics["accuracy"],
            metrics["precision"],
            metrics["recall"],
            metrics["f1"]
        ]
    })

    fig = px.bar(
        metric_df,
        x="Metric",
        y="Score",
        range_y=[0, 1],
        color="Score",
        text_auto=".2f",
        title="Model Performance",
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("### Model Evaluation")

    st.dataframe(
        metric_df,
        use_container_width=True
    )

    st.caption(
        "Metrics are calculated on the held-out test split."
    )

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown("""
<div style="text-align:center;padding:20px;color:#8ca4c8">
    <h3>🛡️ CYBERSHIELD AI</h3>
    <p>Intelligent Network Security Platform</p>
    <small>Python • Streamlit • Scikit-learn • Plotly</small>
</div>
""", unsafe_allow_html=True)
