from imagebite.validators.validations import ConcreteValidation, GenericValidation
from enum import Enum
import time

ResponseType = Enum('ResponseType', ['url', 'image'])        

class PromptResponse:
    
    model: str
    response_type: ResponseType
    __response_image: bytes
    __response_url: str
    execution_time: time.time
    __generic_validations: list[GenericValidation]
    
    @property
    def generic_validations(self) -> list[GenericValidation]:
        return self.__generic_validations
    
    def __init__(self, response_type: ResponseType, response_image: bytes = None, response_url: str = None):
        self.response_type = response_type
        self.__response_image = response_image
        self.__response_url = response_url
        self.execution_time = time.localtime()
        self.__generic_validations = []

    def add_generic_validation(self, evaluation: GenericValidation):
        self.__generic_validations.append(evaluation)
    
    def response(self):
        if (self.response_type == ResponseType.url):
            return self.__response_url
        else:
            return self.__response_image
    
    def is_url(self):
        return (self.response_type == ResponseType.url)

class PromptInstance:

    __preffix = "A photo-realistic color picture of " #the face of "
    __suffix = "Make the face clearly visible. Make the person look at the camera." #The image is taken as a medium long shot.
    
    @property
    def instance_id(self) -> int:
        return self.__id

    @property
    def instance(self) -> str:
        return self.__instance
    
    @property
    def sensitive_communities(self) -> list[str]:
        return self.__sensitive_communities
    
    @property
    def dimensions(self) -> list[str]:
        return self.__dimensions

    @property
    def responses(self) -> list[PromptResponse]:
        return self.__responses
    
    @property
    def validations(self) -> list[ConcreteValidation]:
        return self.__validations

    def __init__(self, instance_id, instance, sensitive_communities = [], dimensions = []):
        self.__id = instance_id
        self.__instance = self.__preffix + instance + self.__suffix
        #self.__instance = instance
        self.__sensitive_communities = sensitive_communities
        self.__dimensions = dimensions
        self.__responses = []
        self.__validations = []
    
    def add_response(self, response: PromptResponse):
        self.__responses.append(response)
    
    def add_validation(self, evaluation: ConcreteValidation):
        self.__validations.append(evaluation)