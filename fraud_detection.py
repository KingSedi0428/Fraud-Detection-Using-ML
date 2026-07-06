import streamlit as st
import pandas as pd
import joblib
import base64
from streamlit_option_menu import option_menu

# Page configuration
st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        /* Main container styling */
        .main {
            padding: 2rem;
        }
        
        /* Card styling */
        .css-1r6slb0 {
            background-color: #f8f9fa;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Header styling */
        .header-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
        }
        
        .header-container h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
        }
        
        .header-container p {
            margin: 0.5rem 0 0 0;
            opacity: 0.9;
            font-size: 1.1rem;
        }
        
        /* Input field styling */
        .stNumberInput, .stSelectbox {
            margin-bottom: 1rem;
        }
        
        /* Button styling */
        .stButton button {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: 600;
            font-size: 1.1rem;
            padding: 0.75rem;
            border: none;
            border-radius: 10px;
            transition: transform 0.2s;
            box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);
        }
        
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(102, 126, 234, 0.4);
        }
        
        /* Result styling */
        .result-container {
            padding: 1.5rem;
            border-radius: 10px;
            margin-top: 1rem;
            text-align: center;
            animation: slideIn 0.5s ease-out;
        }
        
        .result-fraud {
            background-color: #fee2e2;
            border: 2px solid #ef4444;
        }
        
        .result-legit {
            background-color: #dcfce7;
            border: 2px solid #22c55e;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Divider styling */
        hr {
            margin: 2rem 0;
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent, #667eea, transparent);
        }
        
        /* Label styling */
        .input-label {
            font-weight: 600;
            color: #374151;
            margin-bottom: 0.25rem;
        }
        
        /* Two-column layout for inputs */
        .input-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }
        
        @media (max-width: 768px) {
            .input-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-container">
        <h1>🔒 Fraud Detection System</h1>
        <p>Real-time transaction monitoring and risk assessment</p>
    </div>
""", unsafe_allow_html=True)

# Load model with error handling
try:
    model = joblib.load('fraud_detection_pipeline.pkl')
except:
    st.error("⚠️ Model file not found. Please ensure 'fraud_detection_pipeline.pkl' exists in the current directory.")
    st.stop()

# Transaction details section
st.markdown("### 📝 Transaction Details")
st.markdown("Please fill in the transaction information below:")

# Create two columns for better layout
col1, col2 = st.columns(2)

with col1:
    transaction_type = st.selectbox(
        "📊 Transaction Type",
        ["PAYMENT", "TRANSFER", "CASH_OUT", "DEPOSIT"],
        help="Select the type of transaction"
    )
    
    amount = st.number_input(
        "💰 Transaction Amount",
        min_value=0.0,
        value=1000.0,
        step=100.0,
        help="Enter the transaction amount"
    )
    
    oldbalanceOrg = st.number_input(
        "🏦 Sender's Old Balance",
        min_value=0.0,
        value=10000.0,
        step=100.0,
        help="Enter the sender's balance before the transaction"
    )

with col2:
    newbalanceOrig = st.number_input(
        "🏦 Sender's New Balance",
        min_value=0.0,
        value=9000.0,
        step=100.0,
        help="Enter the sender's balance after the transaction"
    )
    
    oldbalanceDest = st.number_input(
        "🏛️ Receiver's Old Balance",
        min_value=0.0,
        value=0.0,
        step=100.0,
        help="Enter the receiver's balance before the transaction"
    )
    
    newbalanceDest = st.number_input(
        "🏛️ Receiver's New Balance",
        min_value=0.0,
        value=0.0,
        step=100.0,
        help="Enter the receiver's balance after the transaction"
    )

# Divider
st.divider()

# Prediction button
if st.button("🔍 Analyze Transaction", type="primary"):
    # Prepare input data
    input_data = pd.DataFrame({
        'type': [transaction_type],
        'amount': [amount],
        'oldbalanceOrg': [oldbalanceOrg],
        'newbalanceOrig': [newbalanceOrig],
        'oldbalanceDest': [oldbalanceDest],
        'newbalanceDest': [newbalanceDest]
    })
    
    # Make prediction
    try:
        prediction = model.predict(input_data)[0]
        
        # Display result with animation and styling
        st.markdown("### 📊 Analysis Result")
        
        if prediction == 1:
            st.markdown("""
                <div class="result-container result-fraud">
                    <h3 style="color: #dc2626; margin: 0;">⚠️ Fraud Detected</h3>
                    <p style="margin: 0.5rem 0 0 0; color: #991b1b;">
                        This transaction shows suspicious patterns and is flagged as potentially fraudulent.
                    </p>
                    <div style="margin-top: 0.5rem; font-size: 0.9rem; color: #7f1d1d;">
                        Risk Level: <strong>High</strong>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="result-container result-legit">
                    <h3 style="color: #16a34a; margin: 0;">✅ Legitimate Transaction</h3>
                    <p style="margin: 0.5rem 0 0 0; color: #166534;">
                        This transaction appears to be normal and legitimate.
                    </p>
                    <div style="margin-top: 0.5rem; font-size: 0.9rem; color: #14532d;">
                        Risk Level: <strong>Low</strong>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        # Additional information
        with st.expander("📋 Transaction Summary"):
            summary_data = {
                "Transaction Type": transaction_type,
                "Amount": f"${amount:,.2f}",
                "Sender Balance Change": f"${oldbalanceOrg - newbalanceOrig:,.2f}",
                "Receiver Balance Change": f"${newbalanceDest - oldbalanceDest:,.2f}"
            }
            st.json(summary_data)
            
    except Exception as e:
        st.error(f"❌ Error during prediction: {str(e)}")

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: #6b7280; font-size: 0.9rem;">
        <p>🔒 All transactions are processed securely</p>
        <p style="margin-top: 0.25rem;">A Fraud Detection System Built with Machine Learning | © 2026</p>
    </div>
""", unsafe_allow_html=True)