from imagebite.model.prompt_instance import PromptInstance
from imagebite.validators.validations import ConcreteValidation

class ValidatedPrompt(PromptInstance):

    @property
    def validations(self):
        return self.__validations
    
    def __init__(self):
        super(ValidatedPrompt, self).__init__()
        self.__validations = []
    
    def add_validation(self, validation: ConcreteValidation):
        self.__validations.append(validation)