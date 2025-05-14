from openai import OpenAI
from datetime import datetime

from src.enums import LOG_DIR


class ChatGPTClient:
    def __init__(self, api_key: str):
        base_url = None
        if not api_key:
            raise Exception("api_key is required")        
        self.model = ModelDefaults.active_model
        self.is_initialized = False
        self.client = OpenAI(api_key=api_key, base_url = base_url)
        self.is_initialized = True

    def ask(self, system_prompt, user_prompt):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}],
            temperature=0,
            stream=True,
            n=1,
        )
        # self.log_result(prompt, completion)
        return completion



    def log_result(self, prompt: str, completion_stream) -> None:
        """Log the prompt and completion to a file."""
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = LOG_DIR / f"llm_results_{date_str}.log"

        with open(log_file, "w") as f:
            f.write("=== PROMPT ===\n")
            f.write(prompt + "\n\n")
            f.write("=== RESPONSE ===\n")
            for chunk in completion_stream:
                if hasattr(chunk.choices[0].delta, 'content'):
                    content = chunk.choices[0].delta.content
                    if content:
                        f.write(content)
            f.write("\n")


class ModelDefaults:
    active_model = "gpt-4o-mini"
    active_model_max_context_length = 128000