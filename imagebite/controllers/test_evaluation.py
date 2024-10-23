from imagebite.model.test_scenario_model import EthicalRequirement
from imagebite.model.prompt import Prompt
from imagebite.validators.abstract_validator import AbstractValidator
from imagebite.validators.concrete_validator_hf import ConcreteValidatorHF
from imagebite.validators.generic_validator import GenericValidator
from imagebite.validators import validator_factory
from imagebite.validators.reasoning_validator import ReasoningValidator

class TestEvaluation:
    
    def __init__(self, test_id, prompts: list[Prompt], requirements: list[EthicalRequirement], perform_generic_evaluations: bool, perform_post_reasoning: bool, api_keys):
        self.__test_id = test_id
        self.__prompts = prompts
        self.__requirements = requirements
        self.__perform_generic_evaluations = perform_generic_evaluations
        self.__perform_post_reasoning = perform_post_reasoning
        self.__api_keys = api_keys
    
    def execute_evaluation(self):
        if self.__perform_generic_evaluations: self.__execute_generic_validation()
        self.__execute_concrete_validations()
    
    def __execute_generic_validation(self):
        validator_service = GenericValidator(**self.__api_keys)
        print(f'performing generic validation of prompts...')
        for i, prompt in enumerate(self.__prompts):
            print(f'evaluating prompt {i}')
            validator_service.validate_responses(prompt)
        print('done')
    
    def __execute_concrete_validations(self):
        if self.__perform_post_reasoning: reasoning_validator_service = ReasoningValidator(**self.__api_keys)
        requirement: EthicalRequirement
        for requirement in self.__requirements:
            #concrete_validator_service: AbstractValidator = validator_factory.validator_factory.create(requirement.discrimination, **self.__api_keys)
            concrete_validator_service = ConcreteValidatorHF(**self.__api_keys)
            print(f'performing concrete {requirement.ethical_concern} validation of prompts...')
            for i, prompt in enumerate(self.__prompts):
                print(f'evaluating prompt {i}')
                if ((requirement.discrimination in prompt.target_discriminations) and
                    (requirement.ethical_concern in prompt.target_ethical_concerns)):
                    concrete_validator_service.validate_responses(self.__test_id, prompt, requirement)
                    if self.__perform_post_reasoning: reasoning_validator_service.validate_responses(prompt)
            print('done')