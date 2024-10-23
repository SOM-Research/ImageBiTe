# -------------------------------------------------------------------------------------------------------------------
# Multi-modal LLM-as-judge
# -------------------------------------------------------------------------------------------------------------------
# Result: a list of quantitative evaluations based on generic conditions addressing different discrimination types
# -------------------------------------------------------------------------------------------------------------------

import base64
import io
from openai import OpenAI
from PIL import Image

from imagebite.model.prompt_instance import PromptResponse, ResponseType


class AbstractValidator:

    def __init__(self, openai_api_key, **ignore):
        self.__api_client = OpenAI(api_key=openai_api_key)
        self.__model = 'gpt-4o-mini'
    
    def validate_responses(self, prompt, **kwargs):
        pass

    def _set_validation_prompt_variables(self) -> str:
        pass

    def _format_response(self, response: str) -> str:
        pass

    def _validate_response(self, response: PromptResponse):
        validation_prompt = self._set_validation_prompt_variables()
        message_payload = self.__get_message_payload(validation_prompt, response)
        validation = self.__query_validation(message_payload)
        return validation
    
    def __query_validation(self, message_payload):
        completion = self.__api_client.chat.completions.create(
            model = self.__model,
            # if no max_tokens provided, default seems to be 16
            # TODO: decide!
            # max_tokens = 30,
            n = 1,
            messages = message_payload)
        result = self._format_response(completion.choices[0].message.content)
        return result
    
    def __get_message_payload(self, validation_prompt, response: PromptResponse):
        image = response.response()
        if (response.response_type == ResponseType.url):
            return [{
                'role': 'user',
                'content': [
                    { 'type': 'text', 'text': validation_prompt },
                    { 'type': 'image_url', 'image_url': { 'url': image } }
                ]
            }]
        else: # is image bytes
            # OpenAI expects a UTF-8 string
            image_file = Image.open(io.BytesIO(image))
            buff = io.BytesIO()
            image_file.save(buff, format="JPEG")
            img_utf8 = base64.b64encode(buff.getvalue()).decode('utf-8')
            return [{
                'role': 'user',
                'content': [
                    { 'type': 'text', 'text': validation_prompt },
                    { 'type': 'image_url', 'image_url': { 'url': f'data:image/jpeg;base64,{img_utf8}'}}
                ]
            }]