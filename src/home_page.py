from datetime import datetime

import streamlit as st

from src.app_settings import APP_SETTINGS
from src.prompt_library import PromptLibrary
from src.gpt_logic import ModelDefaults, PromptPrep
from src.smart_dme_parser import SmartDMEParser
import pandas as pd
import json

def show_wrangler():
    app = APP_SETTINGS

    if not app.openai_apikey:
        st.warning("Please add your OpenAI API key in the .env.")
        return
    
    parser = SmartDMEParser(api_key=app.openai_apikey)

    st.subheader("Input")
    input_container = st.container(border=True)
    col1, col2 = input_container.columns([3, 1])
    col2_container = col2.container()
    with col1:
        user_prompt = st.text_area("User Prompt (Doctor's DME Natural Language Request)", value = "Patient is non-ambulatory and requires hospital bed with trapeze bar and side rails. Diagnosis: late-stage ALS. Order submitted by Dr. Cuddy.")
        system_prompt_from_lib = PromptLibrary.default_system_prompt
        system_prompt = st.text_area("System Prompt", value=system_prompt_from_lib, height=160, help="You can customize the prompt to adjust the way DME requests are parsed into JSON.")

    prompt_with_data = f"{system_prompt} \n```{user_prompt}```"
    estimated_tokens = PromptPrep.estimate_tokens(prompt_with_data)
    col2_container.caption(f"Model: {ModelDefaults.active_model}")
    col2_container.caption(f"Est. input tokens: {estimated_tokens:,} of max {ModelDefaults.active_model_max_context_length:,}")
    temperature = float(col2_container.number_input(f"Temperature", value = 0.0, step=0.1, format="%.1f"))
    max_tokens_input = int(col2_container.number_input(f"Max Tokens", value = ModelDefaults.MODEL_MAX_COMPLETION_TOKENS, min_value=1, max_value=ModelDefaults.MODEL_MAX_COMPLETION_TOKENS, step=100))

    result_container = st.container(border=True)
    result_container.subheader("Output")

    with col2:
        if st.button(":material/send: Run", use_container_width=True):
            if estimated_tokens > ModelDefaults.active_model_max_context_length:
                st.warning(f"Estimated input tokens ({estimated_tokens}) exceed model context length ({ModelDefaults.active_model_max_context_length}). Request might fail or be truncated by the API.")
            
            with st.spinner("Running..."):
                response_data = parser.parse_dme_request(
                    natural_language_query=user_prompt,
                    system_prompt=system_prompt,
                    max_tokens=max_tokens_input,
                    temperature=temperature
                )
                
                app.last_model_response = response_data.raw_content
                result_output_container = result_container.container(border=True)

                if response_data.parsing_error:
                    result_output_container.error(f"Parsing Error: {response_data.parsing_error}")
                    result_output_container.caption("Raw Output from Model:")
                    result_output_container.text(response_data.raw_content)
                elif response_data.structured_data:
                    result_output_container.caption("Successfully parsed JSON output:")
                    result_output_container.json(response_data.structured_data)
                else:
                    result_output_container.warning("No structured data extracted, and no specific parsing error. Check raw output.")
                    result_output_container.caption("Raw Output from Model:")
                    result_output_container.text(response_data.raw_content)

                result_container.caption(f"Actual prompt tokens: {response_data.prompt_tokens},  completion tokens: {response_data.completion_tokens}, execution time: {response_data.execution_time_ms} ms")

                if response_data.structured_data and not response_data.parsing_error:
                    json_to_download = json.dumps(response_data.structured_data, indent=2)
                    result_container.download_button(
                        label="Download Parsed JSON",
                        data=json_to_download,
                        file_name=f"parsed_dme_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                else:
                    result_container.download_button(
                        label="Download Raw Output",
                        data=response_data.raw_content,
                        file_name=f"raw_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )

def page_content():
    st.set_page_config(
        page_title="Medical Device Order Parser",
        page_icon="🏥",
        layout="wide",
        # initial_sidebar_state="expanded"
    )
    ch1, ch2 = st.columns([2,1])
    ch1.markdown("# 🏥 Medical Device Order Parser")
    st.info("Convert unstructured medical device orders into structured JSON format. This tool extracts key information such as device type, provider, diagnosis, and specific attributes.")
    show_wrangler()

page_content()

