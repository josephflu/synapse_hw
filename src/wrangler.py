import streamlit as st

from src.app_settings import APP_SETTINGS
from src.prompt_library import PromptLibrary, PromptPrep
from src.gpt_logic import ChatGPTClient


def show_wrangler():
    app = APP_SETTINGS

    prompt  = PromptLibrary.default_prompt


    # Analysis Results Section
    if not app.openai_apikey:
        st.warning("Please add your OpenAI API key in Settings to use this feature.")
        return

    result_container = st.container(border=True)
    col1, col2 = result_container.columns([3, 1])
    col2_container = col2.container()
    with col1:
        edited_prompt = st.text_area("Prompt", value=prompt, height=160, help="You can customize the prompt to analyze the jobs. "
                                     "Edits will override the default prompt and are stored in _bridgectl/config/user_llm_prompts.yml_. "
                                     "You can also manually edit this file.")
    dme_request = st.text_area("DME Natural Language Request", value = "Patient is non-ambulatory and requires hospital bed with trapeze bar and side rails. Diagnosis: late-stage ALS. Order submitted by Dr. Cuddy.")

    prompt_with_data = f"{edited_prompt} \n```{dme_request}```"
    estimated_tokens = PromptPrep.estimate_tokens(prompt_with_data)
    col2_container.caption(f"Model: gpt-4o-mini")
    col2_container.caption(f"Est. Tokens: {estimated_tokens:,} of max {PromptPrep.max_prompt_token_length_o1mini:,}")

    with col2:
        cont = st.container()
        prompt_with_data = f"{prompt} \n```{dme_request}```"
        if cont.button(":material/send: Run Analysis", use_container_width=True):
            gpt = ChatGPTClient(app.openai_apikey)
            if estimated_tokens > PromptPrep.max_prompt_token_length_o1mini:
                st.warning(f"Prompt will be truncated to max tokens.")

            with st.spinner("Analyzing jobs..."):
                completion_stream = gpt.ask(prompt_with_data)
                result_container.write_stream(completion_stream)
        else:
            result_container.info("Analyze DME request.")
                

def page_content():
    st.set_page_config(
        page_title="The Prompt Wrangler",
        page_icon="📊",
        layout="wide",
    )
    ch1, ch2 = st.columns([2,1])
    ch1.markdown("# :material/work: The Prompt Wrangler - Synapse Health Homework")
    st.info("This utility allows you to extract structured data from a natural language DME request provided by a doctor.")

    show_wrangler()


page_content()

