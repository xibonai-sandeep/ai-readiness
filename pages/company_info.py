import streamlit as st


def app():
    st.markdown("<h2 style='color: #4b0082;'>Company Information</h2>", unsafe_allow_html=True)
    # Initialize session state variables if they don't exist
    if "company_info" not in st.session_state:
        st.session_state.company_info = {}

    # Input fields for company information
    industry = st.selectbox(
        "Industry",
        ["Technology", "Healthcare", "Finance", "Retail", "Manufacturing", "Other"],
    )
    size = st.selectbox(
        "Company Size",
        [
            "Small (1-50 employees)",
            "Medium (51-500 employees)",
            "Large (501+ employees)",
        ],
    )
    country = st.text_input("Country")

    if st.button("Next"):
        # Store company information in session state
        st.session_state.company_info = {
            "industry": industry,
            "size": size,
            "country": country,
        }
        st.success("Company information saved. Please proceed to the Assessment page.")
