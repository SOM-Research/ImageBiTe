# ---------------------------------------------------------------------------------
# Factory/builder for HuggingFace services
# ---------------------------------------------------------------------------------

class HuggingFaceT2IServiceBuilder:
    def __init__(self, model, inference_api_url):
        self.__instance = None
        self.__model = model
        self.__inference_api_url = inference_api_url
    
    def __call__(self, huggingface_api_key, **_ignored):
        if not self.__instance:
            self.__instance = HuggingFaceT2IService(huggingface_api_key, self.__model, self.__inference_api_url)
        return self.__instance


# ---------------------------------------------------------------------------------
# HuggingFace services
# ---------------------------------------------------------------------------------

from imagebite.model.prompt_instance import PromptResponse, ResponseType
from imagebite.t2i_services.t2i_service import T2IService
import requests


# ---------------------------------------------------------------------------------
# Abstract service
# ---------------------------------------------------------------------------------

class HuggingFaceService(T2IService):
    
    def __init__(self, huggingface_api_key, model, inference_api_url):
        self._api_url = inference_api_url
        self._headers = {'Authorization': f'Bearer {huggingface_api_key}', 'x-use-cache': 'false'}
        self.provider = 'HuggingFace'
        self.model = model

# ---------------------------------------------------------------------------------
# Text-to-image generation service
# ---------------------------------------------------------------------------------

class HuggingFaceT2IService(HuggingFaceService):

    def execute_prompt(self, prompt) -> PromptResponse:
        payload = {'inputs': prompt}
        response = requests.post(self._api_url, headers=self._headers, json=payload)
        #image = Image.open(io.BytesIO(response.content))
        image = response.content
        # add the image as bytes to the prompt response;
        # it will be managed / processed accordingly by the validator and the IO manager
        result = PromptResponse(response_type=ResponseType.image, response_image=image)
        return result