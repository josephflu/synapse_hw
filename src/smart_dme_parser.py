from typing import Dict, Any
import json
from .gpt_logic import ChatGPTClient, ModelResponse, ModelDefaults
from .prompt_library import PromptLibrary # Assuming this file and class/object exist


class MedicalOrderProcessor:

    def parse(self, text: str) -> Dict[str, Any]:
        pass

class SmartDMEResponse:
    def __init__(self, structured_data: dict, raw_content: str, prompt_tokens: int, completion_tokens: int, execution_time_ms: int, parsing_error: str):
        self.structured_data = structured_data
        self.raw_content = raw_content
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.execution_time_ms = execution_time_ms
        self.parsing_error = parsing_error

class SmartDMEParser:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("OpenAI API key is required.")
        self.client = ChatGPTClient(api_key=api_key)

    def parse_dme_request(
        self,
        natural_language_query: str,
        system_prompt: str = None,
        max_tokens: int = None, # Will use ModelDefaults.MODEL_MAX_COMPLETION_TOKENS if None
        temperature: float = 0  # Defaulting to 0 for deterministic output
    ) -> SmartDMEResponse:  
        """
        Takes a natural language DME request and returns structured JSON data.
        Also returns token usage and execution time.
        """
        if system_prompt is None:
            system_prompt = PromptLibrary.default_system_prompt # Make sure this attribute exists

        # Use default from ModelDefaults if not provided,
        # gpt_logic.ask already handles capping this, so we pass it through
        # or let gpt_logic.ask use its own default if None is passed here.
        # For clarity, let's explicitly pass it or its default.
        effective_max_tokens = max_tokens if max_tokens is not None else ModelDefaults.MODEL_MAX_COMPLETION_TOKENS

        model_resp: ModelResponse = self.client.ask(
            system_prompt=system_prompt,
            user_prompt=natural_language_query,
            max_tokens=effective_max_tokens,
            temperature=temperature
        )

        parsed_json = None
        error_message = None

        try:
            # Attempt to find JSON within potentially larger string (e.g. if LLM adds explanations)
            # A simple way is to find the first '{' and last '}'
            # More robust methods might be needed if the output is very noisy.
            json_start_index = model_resp.content.find('{')
            json_end_index = model_resp.content.rfind('}')

            if json_start_index != -1 and json_end_index != -1 and json_end_index > json_start_index:
                json_string = model_resp.content[json_start_index : json_end_index+1]
                parsed_json = json.loads(json_string)
            else:
                error_message = "No JSON object found in the model's response."
                # Fallback: try to parse the whole content if no clear delimiters are found
                try:
                    parsed_json = json.loads(model_resp.content)
                    error_message = None # Succeeded with whole content
                except json.JSONDecodeError:
                    # If this also fails, stick with the "No JSON object found" or create a more specific one.
                    if not error_message: # if it was None before
                         error_message = "Failed to decode JSON from the model's response."

        except json.JSONDecodeError as e:
            error_message = f"JSON decoding failed: {str(e)}. Raw content: {model_resp.content}"
        except Exception as e:
            error_message = f"An unexpected error occurred during parsing: {str(e)}"

        return SmartDMEResponse(    
            structured_data=parsed_json,
            raw_content=model_resp.content,
            prompt_tokens=model_resp.prompt_tokens,
            completion_tokens=model_resp.completion_tokens,
            execution_time_ms=model_resp.execution_time_ms,
            parsing_error=error_message
        )
        


