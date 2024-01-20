import openai
import re
from typing import Any

from edsl import CONFIG
from edsl.language_models import LanguageModel

openai.api_key = CONFIG.get("OPENAI_API_KEY")
from openai import AsyncOpenAI

# client = AsyncOpenAI()


class LanguageModelOpenAIFour(LanguageModel):
    """
    Child class of LanguageModel for interacting with OpenAI GPT-4 model.
    """

    client = AsyncOpenAI()

    _model_ = "gpt-4-1106-preview"
    _parameters_ = {
        "temperature": 0.5,
        "max_tokens": 1000,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "use_cache": True,
    }

    async def async_execute_model_call(
        self, user_prompt: str, system_prompt: str = ""
    ) -> dict[str, Any]:
        """Calls the OpenAI API and returns the API response."""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
        )
        return response.model_dump()

    @staticmethod
    def parse_response(raw_response: dict[str, Any]) -> str:
        """Parses the API response and returns the response text."""
        response = raw_response["choices"][0]["message"]["content"]
        pattern = r"^```json(?:\\n|\n)(.+?)(?:\\n|\n)```$"
        match = re.match(pattern, response, re.DOTALL)
        if match:
            return match.group(1)
        else:
            return response


if __name__ == "__main__":
    import doctest

    doctest.testmod()