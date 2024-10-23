from imagebite.model.prompt import Prompt
from imagebite.model.test_scenario_model import EthicalRequirement, TestScenario
from random import sample

class TestGeneration:

    # @property
    # def prompts(self) -> list[Prompt]:
    #     return self.__prompts
    
    # @property
    # def ethical_requirements(self) -> list[EthicalRequirement]:
    #     return self.test_scenario.ethical_requirements

    @property
    def num_instances_generated(self):
        num_instances = 0
        if len(self.__prompts) > 0:
            prompt: Prompt
            for prompt in self.__prompts:
                num_instances = num_instances + len(prompt.instances)
        return num_instances

    def __init__(self, scenario: TestScenario):
        self.__test_scenario = scenario
        self.__ethical_requirements = scenario.ethical_requirements
    
    def generate_scenario(self, prompts: list[Prompt]) -> list[Prompt]:
        self.__select_prompts(prompts)
        self.__instantiate_prompts()
        return self.__prompts
    
    def __select_prompts(self, prompts: list[Prompt]):
        result = []
        #unique_discriminations = set([req.discrimination for req in self.__ethical_requirements])
        req: EthicalRequirement
        for req in self.__ethical_requirements:
        #for discrimination in unique_discriminations:
            discrimination = req.discrimination
            ethical_concern = req.ethical_concern
            #temp = [prompt for prompt in prompts if prompt.ethical_concern == concern]
            temp = [prompt for prompt in prompts if (discrimination in prompt.target_discriminations) and (ethical_concern in prompt.target_ethical_concerns)]
            # and then select according to num templates specified
            result = result + self.__sample_list(temp)
        self.__prompts = set(result) # remove repeated prompts; some may address many discriminations and concerns
    
    def __sample_list(self, prompt_list: list[Prompt]):
        if len(prompt_list) > self.__test_scenario.num_templates: prompt_list = sample(prompt_list, self.__test_scenario.num_templates)
        return prompt_list
    
    def __instantiate_prompts(self):
        for prompt in self.__prompts: prompt.instantiate(self.__test_scenario.ethical_concerns, self.__test_scenario.dimensions)
    
    # def __instantiate_prompts(self):
    #     req: EthicalRequirement
    #     for req in self.__ethical_requirements:
    #         prompt: Prompt
    #         for prompt in self.__prompts:
    #             if (prompt.ethical_concern == req.ethical_concern):
    #                 prompt.instantiate(req.markup, req.communities)