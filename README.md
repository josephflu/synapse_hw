#  The Prompt Wrangler

## Background

Doctors submit unstructured clinical notes (e.g., _"Patient needs a CPAP with full face mask and humidifier. AHI > 20. Ordered by Dr. Cameron."_). This tool helps extract structured data (like JSON) using an LLM.

The goal is to provide an interface to:
*   Input system and user prompts.
*   Adjust LLM parameters (temperature, max_tokens).
*   Send to OpenAI and display the structured output.
*   Show token usage and response time.

This project is a Streamlit application that fulfills these requirements.

## 🚀 How to Run

1.  **Prerequisites**:
    *   Python 3.12+
    *   An OpenAI API Key
2.  **Setup**:
    ```bash
    # Install dependencies
    pip install streamlit openai python-dotenv
    # Create a .env file in the project root with your OPENAI_API_KEY
    # Example: OPENAI_API_KEY="YOUR_API_KEY_HERE"
    ```
3.  **Launch**:
    ```bash
    streamlit run src/wrangler.py
    ```
    The app will open in your browser.

## 📝 How to Use

1.  **API Key**: Ensure your `OPENAI_API_KEY` is in a `.env` file at the project root.
2.  **Prompts**: Edit the "System Prompt" (LLM instructions) and "User Prompt" (doctor's note).
3.  **Parameters**: Adjust `Temperature` and `Max Tokens` in the right sidebar.
4.  **Run**: Click the ":material/send: Run" button.
5.  **Results**: View the "Structured Output" and performance metrics (tokens, time).

## 📂 Project Files

*   `src/wrangler.py`: Main Streamlit application.
*   `src/gpt_logic.py`: OpenAI client and data handling (`ChatGPTClient`, `ModelResponse`).
*   `src/app_settings.py`: Loads API key (from `.env`).
*   `src/prompt_library.py`: Provides default prompts.

## 🔍 Example

**Input (User Prompt):**
`Patient requires a full face CPAP mask with humidifier due to AHI > 20. Ordered by Dr. Cameron.`

**Target Output (with a suitable System Prompt for JSON):**
```json
{
  "device": "CPAP",
  "mask_type": "full face",
  "add_ons": ["humidifier"],
  "qualifier": "AHI > 20",
  "ordering_provider": "Dr. Cameron"
}
```
