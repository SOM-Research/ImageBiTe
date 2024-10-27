from imagebite.model.prompt import Prompt
from imagebite.model.prompt_instance import PromptInstance
from imagebite.validators.validations import ConcreteValidation


class ConcreteValidationView:

    @property
    def ethical_concern(self):
        return self.__ethical_concern
    
    @ethical_concern.setter
    def ethical_concern(self, value):
        if value is None: self.__ethical_concern = ''
        else: self.__ethical_concern = value

    @property
    def dimension_type(self):
        return self.__dimension_type
    
    @dimension_type.setter
    def dimension_type(self, value):
        if value is None: self.__dimension_type = ''
        else: self.__dimension_type = value

    def __init__(self, prompt: Prompt, instance: PromptInstance, validation: ConcreteValidation):
        self.validator_responses = ''
        self.model = validation.model
        self.prompt_id = prompt.prompt_id
        self.ethical_concern = prompt.ethical_concern
        self.sensitive_communities = instance.sensitive_communities
        self.dimension_type = prompt.dimension
        self.dimension_values = instance.dimensions
        self.instance = instance.instance
        self.evaluated_discrimination = validation.discrimination
        self.evaluated_ethical_concern = validation.ethical_concern
        self.underrepresented_communities = ''
        self.exnominated_communities = ''
        self.stereotyped_communities = ';'.join([item.sensitive_community for item in validation.stereotyped_communities])
        self.underrepresented_communities = ';'.join([item.sensitive_community + ' (' + str(item.actual_occurrences) + ',{:6.2f}'.format(item.actual_distribution*100) + '%)' for item in validation.underrepresented_communities])
        self.exnominated_communities = ';'.join([item.sensitive_community for item in validation.exnominated_communities])
        self.reasoning = validation.reasoning
        self.totals = ';'.join([item.sensitive_community + ' (' + str(item.actual_occurrences) + ',{:6.2f}'.format(item.actual_distribution*100) + '%)' for item in validation.sensitive_communities_distribution])
            

    def to_dict(self):
        return {
            'ID': self.prompt_id,
            'Model': self.model,
            'Concern': self.ethical_concern,
            'Community': ';'.join(self.sensitive_communities),
            'Dimension Type': self.dimension_type,
            'Dimension': ';'.join(self.dimension_values),
            'Instance': self.instance,
            'Discrimination Evald.': self.evaluated_discrimination,
            'Concern Evald.': self.evaluated_ethical_concern,
            'Under-represented Comms': self.underrepresented_communities,
            'Ex-nominated Comms': self.exnominated_communities,
            'Stereotyped Comms': self.stereotyped_communities,
            'LLM-as-judge Reasoning': self.reasoning,
            'Total Occurrences': self.totals
        }

class ConcreteValidationDecorator:

    @property
    def validations(self):
        return self.__validations

    def __init__(self, prompt: Prompt):
        self.__validations = []
        instance: PromptInstance
        for instance in prompt.instances:
            for validation in instance.validations:
                self.__validations.append(ConcreteValidationView(prompt, instance, validation))