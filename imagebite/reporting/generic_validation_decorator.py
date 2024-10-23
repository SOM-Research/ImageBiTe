from imagebite.model.prompt import Prompt
from imagebite.model.prompt_instance import PromptInstance, PromptResponse
from imagebite.validators.validations import GenericValidation


class GenericValidationView:

    def __init__(self, prompt: Prompt, instance: PromptInstance, validation: GenericValidation):
        self.prompt_id = prompt.prompt_id
        self.instance = instance.instance
        self.discrimination = validation.discrimination
        self.name = validation.name
        self.response = validation.response
        self.reasoning = validation.reasoning
        self.evaluation = validation.evaluation

    def to_dict(self):
        return {
            'ID': self.prompt_id,
            'Instance': self.instance,
            'Discrimination': self.discrimination,
            'Name': self.name,
            'LLM-as-judge Response': self.response,
            'LLM-as-judge Reasoning': self.reasoning,
            'LLM-as-judge Evaluation': self.evaluation
        }

class GenericValidationDecorator:

    @property
    def validations(self):
        return self.__validations

    def __init__(self, prompt: Prompt):
        self.__validations = []
        instance: PromptInstance
        for instance in prompt.instances:
            response: PromptResponse
            for response in instance.responses:
                for validation in response.generic_validations:
                    self.__validations.append(GenericValidationView(prompt, instance, validation))