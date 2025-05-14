import streamlit as st

class PageUtil:
    @staticmethod
    def set_page_config(page_title: str, page_header: str = None, skip_image: bool = False):
        # st.logo("src/page/assets/tableau_icon_24.png")
        st.set_page_config(
            page_title=page_title,
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        st.write(f"# {page_header}")
