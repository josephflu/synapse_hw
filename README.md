#  The Prompt Wrangler - 


## Background

Doctors submit unstructured clinical notes (e.g., _"Patient needs a CPAP with full face mask and humidifier. AHI > 20. Ordered by Dr. Cameron."_). This tool helps extract structured data (JSON) using an LLM.
This utility will help fine tune LLM prompts to optimize conversion of NLP input to structured output.

The goal is to provide an interface to:
*   Input system and user prompts.
*   Adjust LLM parameters (temperature, max_tokens).
*   Send to the LLM model and display the structured output.
*   Show token usage and response time.
*   

##  How to Run

1.  **Prerequisites**:
    *   Python 3.12+
    *   An OpenAI API Key
2.  **Setup**:
    ```bash
    # Install dependencies
    pip install -r requirements.txt
    # Create a .env file in the project root with your OPENAI_API_KEY, (see .env.example)
    ```
3.  **Launch**:
    ```bash
    streamlit run src/wrangler.py
    ```
    The app will open in your browser at http://localhost:8502

## How to Use

-  **Prompts**: Edit the "System Prompt" (LLM instructions) and "User Prompt" (doctor's note).
-  **Parameters**: Adjust `Temperature` and `Max Tokens` in the right sidebar.
-  **Run**: Click the "Run" button.
-  **Results**: View the "Structured Output" and performance metrics (tokens, time).

## Project Files

*   `src/wrangler.py`: Main Streamlit application.
*   `src/gpt_logic.py`: OpenAI client and data handling (`ChatGPTClient`, `ModelResponse`).
*   `src/app_settings.py`: Loads API key (from `.env`).
*   `src/prompt_library.py`: Provides default prompts.



## Next Steps
There are quite a few next steps we could take for this project.
#### Features to Add
* Add the ability to import CSV or json files for easier bulk processing and bulk testing
* Build a testing framework to measure performance of the system and score result confidence (measure LLM performance, and prompt performance, and other parameters)
* Keep track of historical Prompts and score those Prompts based on results.
#### Additional Data
* Add a confidence score to the results
* Historical scores of various prompts and LLMs
#### System Improvements
* Build an API that can be called by a production system to parse NPL DME queries into json
* Build an Agent in Langchain which can use a React loop to iterate on the results and verify correctness, check input against multiple LLMs, guarantee correct response format, etc.
### Architecture Improvements
* break application into layers (UI, logic, data layer) for more modular design as we scale.
