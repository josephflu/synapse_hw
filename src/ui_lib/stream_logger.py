import traceback

from src.models import LoggerInterface
import streamlit as st

class StreamLogger(LoggerInterface):
    def __init__(self, container = None, progress_bar = None):
        self.container = container
        self.progress_bar = progress_bar

    def info(self, msg = ""):
        if self.container:
            self.container.text(msg)
        else:
            st.text(msg)

    def warning(self,  msg: str):
        if self.container:
            self.container.warning(msg)
        else:
            st.warning(msg)

    def error(self, msg, ex: Exception = None):
        # ex_string = traceback.print_exc()
        if self.container:
            self.container.error(msg)
        else:
            st.error(f"ERROR: {msg}")

    def progress(self, value: int):
        if self.progress_bar:
            self.progress_bar.progress(value)
