from dataclasses import dataclass

from openai import OpenAI
from openai import OpenAIError


@dataclass
class ModelResponse:
    content: str = None
    prompt_tokens: int = 0
    completion_tokens: int = 0


class ChatGPTClient:
    def __init__(self, api_key: str):
        base_url = None
        if not api_key:
            raise Exception("api_key is required")        
        self.is_initialized = False
        self.client = OpenAI(api_key=api_key, base_url = base_url)
        self.is_initialized = True

    def ask(self, system_prompt, user_prompt) -> ModelResponse:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}]
        try:
            resp = self.client.chat.completions.create(
                model = ModelDefaults.active_model,
                messages = messages,
                temperature = 0,
                n=1,
                timeout=15 # seconds
            )
        except OpenAIError as e:
            raise Exception("OpenAI API error", e)
            # self.logger.error("OpenAI API error", exc_info=e)

        mr = ModelResponse()
        mr.content = resp.choices[0].message.content.strip()
        mr.prompt_tokens = resp.usage.prompt_tokens
        mr.completion_tokens = resp.usage.completion_tokens
        return mr


class ModelDefaults:
    active_model = "gpt-4o-mini"
    active_model_max_context_length = 128000


class PromptPrep:
    @staticmethod
    def estimate_tokens(prompt: str) -> int:
        """Estimate the number of tokens in a string."""
        tokens_per_char = 0.25  # rough estimate of tokens per character for English text
        return int(len(prompt) * tokens_per_char)