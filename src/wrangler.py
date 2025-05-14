import streamlit as st

from src.app_settings import APP_SETTINGS
from src.prompt_library import PromptLibrary
from src.gpt_logic import ChatGPTClient, ModelDefaults, PromptPrep


def show_wrangler():
    app = APP_SETTINGS

    # Analysis Results Section
    if not app.openai_apikey:
        st.warning("Please add your OpenAI API key in the .env.")
        return

    result_container = st.container(border=True)
    col1, col2 = result_container.columns([3, 1])
    col2_container = col2.container()
    with col1:
        user_prompt = st.text_area("User Prompt (Doctor's DME Natural Language Request)", value = "Patient is non-ambulatory and requires hospital bed with trapeze bar and side rails. Diagnosis: late-stage ALS. Order submitted by Dr. Cuddy.")
        system_prompt = st.text_area("System Prompt", value=PromptLibrary.default_system_prompt, height=160, help="You can customize the prompt to adjust the way DME requests are parsed into JSON.")

    result_container.markdown("### Structured Output")
    prompt_with_data = f"{system_prompt} \n```{user_prompt}```"
    estimated_tokens = PromptPrep.estimate_tokens(prompt_with_data)
    col2_container.caption(f"Model: {ModelDefaults.active_model}")
    col2_container.caption(f"Est. Tokens: {estimated_tokens:,} of max {ModelDefaults.active_model_max_context_length:,}")

    with col2:
        cont = st.container()
        if cont.button(":material/send: Run", use_container_width=True):
            gpt = ChatGPTClient(app.openai_apikey)
            if estimated_tokens > ModelDefaults.active_model_max_context_length:
                st.warning(f"Prompt will be truncated to max tokens.")
            with st.spinner("Running..."):
                model_resp = gpt.ask(system_prompt, user_prompt)
                result_output = result_container.container(border=True)
                result_output.write(model_resp.content)
                result_container.caption(f"Actual prompt tokens: {model_resp.prompt_tokens},  completion tokens: {model_resp.completion_tokens}")
        else:
            result_output = result_container.container(border=True)
            result_output.caption("")


def page_content():
    st.set_page_config(
        page_title="The Prompt Wrangler",
        page_icon="📊",
        layout="wide",
        # initial_sidebar_state="expanded"
    )
    ch1, ch2 = st.columns([2,1])
    ch1.markdown("# :material/work: The Prompt Wrangler - Synapse Health")
    st.info("This utility allows you to extract structured data from a natural language DME request provided by a doctor.")

    show_wrangler()


page_content()

