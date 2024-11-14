import streamlit as st
from pages import company_info, assessment, results

st.set_page_config(page_title="AI Readiness Assessment", layout="wide")

# Load custom CSS
with open("styles/custom.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    st.markdown("<div class='xibonai-title'>XIBONAI</div>", unsafe_allow_html=True)
    st.title("AI Readiness Assessment")
    
    # Remove the sidebar navigation
    pages = {
        "Company Information": company_info,
        "Assessment": assessment,
        "Results": results,
    }
    
    # Add the navigation to the main content area
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    
    # Create tabs for navigation
    selected_page = st.tabs(list(pages.keys()))
    
    # Display the content of the selected page
    for i, (page_name, page_function) in enumerate(pages.items()):
        with selected_page[i]:
            page_function.app()
    
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()