"""
Debug script for running Streamlit apps with PyCharm debugging
"""
import sys

if __name__ == "__main__":
    # Add streamlit command line arguments
    sys.argv = ["streamlit", "run", "src/home_page.py"]

    # Import streamlit cli only after setting argv
    import streamlit.web.cli as stcli

    # Use the official CLI entry point
    stcli.main()