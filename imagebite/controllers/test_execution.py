from imagebite.model.test_scenario_model import TestScenario
from imagebite.model.prompt import Prompt
from imagebite.t2i_services import t2i_factory
from imagebite.t2i_services.t2i_service import T2IService
import time

class TestExecution:
    
    def __init__(self, scenario: TestScenario, prompts: list[Prompt], api_keys):
        self.__scenario = scenario
        self.__prompts = prompts
        self.__api_keys = api_keys
    
    def execute_scenario(self):
        for model in self.__scenario.llms:
            self.__query_model(model)
    
    def __query_model(self, model: str):
        print(f'querying {model}...')
        t2i_service: T2IService = t2i_factory.factory.create(model, **self.__api_keys)
        prompt: Prompt
        print(f'running {len(self.__prompts)} prompts.')
        num_instances = sum(len(p.instances) for p in self.__prompts)
        print(f'{num_instances} instances.')
        for i, prompt in enumerate(self.__prompts):
            print(f'running prompt {i+1}')
            n_attempts = self.__scenario.num_retries
            while n_attempts > 0:
                try:
                    prompt.execute(model, t2i_service, self.__scenario.num_samples)
                    break
                except Exception as ex:
                    n_attempts = n_attempts - 1
                    if (n_attempts == 0):
                        pass
                    else:
                        time.sleep(1) # sleep for 1 second to allow the model to restore
        print('done')