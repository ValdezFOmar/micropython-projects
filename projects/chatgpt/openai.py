import urequests as requests

from micropython import const

SUCCEED_STATUS_CODE = const(200)


class OpenAIRequest:
    OPEN_AI_URL = const("https://api.openai.com/v1/chat/completions")

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key
        self.waiting_for_request = False

    def get_chatgpt_response(self, promp: str) -> str:
        response = self.make_openai_resquest(promp)

        if response.status_code != SUCCEED_STATUS_CODE:  # type: ignore
            return "An error occurred"

        data = response.json()
        content = data["choices"][0]["message"]["content"]
        return content

    def make_openai_resquest(self, prompt: str) -> requests.Response:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}",
        }
        post_data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": f"{prompt}",
                },
            ],
            "temperature": 0.7,
        }

        self.waiting_for_request = True
        response = requests.post(
            self.OPEN_AI_URL,
            json=post_data,
            headers=headers,
        )
        self.waiting_for_request = False
        return response
