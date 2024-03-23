import openai
import re
from typing import Any
from edsl import CONFIG
from openai import AsyncOpenAI
from edsl.enums import LanguageModelType, InferenceServiceType
from edsl.language_models import LanguageModel

LanguageModelType.GPT_4.value


def create_openai_model(model_name, model_class_name) -> LanguageModel:
    openai.api_key = CONFIG.get("OPENAI_API_KEY")

    class LLM(LanguageModel):
        """
        Child class of LanguageModel for interacting with OpenAI models
        """

        _inference_service_ = InferenceServiceType.OPENAI.value
        _model_ = model_name
        _parameters_ = {
            "temperature": 0.5,
            "max_tokens": 1000,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "use_cache": True,
        }
        client = AsyncOpenAI()

        def get_headers(self) -> dict[str, Any]:
            from openai import OpenAI

            client = OpenAI()
            response = client.chat.completions.with_raw_response.create(
                messages=[
                    {
                        "role": "user",
                        "content": "Say this is a test",
                    }
                ],
                model=self.model,
            )
            return dict(response.headers)

        def get_rate_limits(self) -> dict[str, Any]:
            try:
                headers = self.get_headers()
            except Exception as e:
                return {
                    "rpm": 10_000,
                    "tpm": 2_000_000,
                }
            else:
                return {
                    "rpm": int(headers["x-ratelimit-limit-requests"]),
                    "tpm": int(headers["x-ratelimit-limit-tokens"]),
                }

        async def async_execute_model_call(
            self, user_prompt: str, system_prompt: str = ""
        ) -> dict[str, Any]:
            """Calls the OpenAI API and returns the API response."""
            with open("test.txt","w") as f:
                f.write(self._model_)
                f.close()
            try:
                if self.model == "gpt-4-vision-preview":
                    messages=[
                        {
                        "role": "user",
                        "content": [
                            {
                            "type": "text",
                            "text": user_prompt,
                            },
                            {
                            "type": "image_url",
                            "image_url": {
                                "url": "https://media.cnn.com/api/v1/images/stellar/prod/141111134114-01-obama-asia-1111.jpg?q=w_3242,h_2440,x_0,y_0,c_fill",
                            },
                            },
                        ],
                        }
                    ]
                else:
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ]
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    top_p=self.top_p,
                    frequency_penalty=self.frequency_penalty,
                    presence_penalty=self.presence_penalty,
                )
            except Exception as e:
                with open("test1.txt","w") as f:
                    f.write(user_prompt)
                    f.close()
            with open("test.txt2","w") as f:
                f.write(user_prompt)
                f.close() 
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

    LLM.__name__ = model_class_name

    return LLM


if __name__ == "__main__":
    import doctest

    doctest.testmod()

               
    