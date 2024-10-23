# ---------------------------------------------------------------------------------
# Factory/builder for OpenAI services
# ---------------------------------------------------------------------------------

class OpenAIT2IServiceBuilder:
    def __init__(self, model):
        self.__instance = None
        self.__model = model
    
    def __call__(self, openai_api_key, **_ignored):
        if not self.__instance:
            self.__instance = OpenAIT2IService(openai_api_key, self.__model)
        return self.__instance


# ---------------------------------------------------------------------------------
# OpenAI services
# ---------------------------------------------------------------------------------

from imagebite.model.prompt_instance import PromptResponse, ResponseType
from imagebite.t2i_services.t2i_service import T2IService
from openai import OpenAI

# ---------------------------------------------------------------------------------
# Abstract service
# ---------------------------------------------------------------------------------

class OpenAIService(T2IService):

    @property
    def api_client(self):
        return self.__api_client
    
    def __init__(self, openai_api_key, model):
        self.__api_client = OpenAI(api_key=openai_api_key)
        self.provider = 'OpenAI'
        self.model = model

# ---------------------------------------------------------------------------------
# Text-to-image generation service
# ---------------------------------------------------------------------------------

class OpenAIT2IService(OpenAIService):

    def execute_prompt(self, prompt) -> PromptResponse:
        response = self.api_client.images.generate(
            model = self.model,
            prompt = prompt,
            n = 1,
        )
        result = PromptResponse(response_type=ResponseType.url, response_url=response.data[0].url)
        return result
        # return {
        #     'revised_prompt': response.data[0].revised_prompt,
        #     'image_url': response.data[0].url
        # }