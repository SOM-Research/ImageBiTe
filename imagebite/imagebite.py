from enum import Enum
from imagebite.controllers.reporting import ReportingManager
import imagebite.io_managers.json_io_manager as ScenarioIOManager
import imagebite.io_managers.prompt_io_manager as PromptIOManager
from imagebite.controllers.test_generation import TestGeneration
from imagebite.controllers.test_execution import TestExecution
from imagebite.controllers.test_evaluation import TestEvaluation
from datetime import datetime
import imagebite.io_managers.file_manager as FileManager
import imagebite.io_managers.secrets as Secrets



class RequirementsFileRequiredException(Exception):
    '''Sorry, you must provide a requirements file name.'''

class WrongStateException(Exception):
    '''Sorry, you haven't followed the expected workflow. The proper invoking sequence is: init LangBite, generate, execute and report.'''

# very simple state machine
# 0 = initiated
# 1 = scenarios loaded and prompts selected
# 2 = tests executed
# 3 = evaluations collected
StateMachineKind = Enum('StateMachine', 'initiated generated executed evaluated')

class ImageBiTe:

    # ---------------------------------------------------------------------------------
    # Public and private properties
    # ---------------------------------------------------------------------------------

    @property
    def requirements_file(self):
        return self.__requirements_file
    
    @requirements_file.setter
    def requirements_file(self, value):
        self.__requirements_file = value

    @property
    def requirements_dict(self):
        return self.__requirements_dict

    @requirements_dict.setter
    def requirements_dict(self, value):
        self.__requirements_dict = value

    @property
    def __requirements_file_empty(self):
        return (not self.__requirements_file or not self.__requirements_file.strip()) and not self.requirements_dict

    @property
    def __current_status(self):
        return self.__current_internal_status
    
    @__current_status.setter
    def __current_status(self, value):
        self.__current_internal_status = value


    # ---------------------------------------------------------------------------------
    # Internal and auxiliary methods
    # ---------------------------------------------------------------------------------

    def __init__(self, prompts_path = None, file = None, file_dict = None, save_generated_images = False):
        self.__api_keys = Secrets.load_api_keys()
        self.__requirements_file = file
        self.__requirements_dict = file_dict
        self.__save_generated_images = save_generated_images
        if not prompts_path:
            self.__prompts_path = FileManager.get_resource_path('prompts_t2i_en_us.csv')
        else:
            self.__prompts_path = prompts_path
        self.__current_status = StateMachineKind.initiated
        self.prompts = []

    def __update_figures(self, test_generation: TestGeneration):
        self.__num_prompts = len(self.prompts)
        self.__num_instances = test_generation.num_instances_generated
    
    # ---------------------------------------------------------------------------------
    # Methods for generating, executing and reporting test scenarios
    # ---------------------------------------------------------------------------------

    def execute_full_scenario(self):
        self.generate()
        self.execute()
        self.evaluate()
        self.report()

    def generate(self):
        if (self.__current_status != StateMachineKind.initiated): raise WrongStateException
        if (self.__requirements_file_empty): raise RequirementsFileRequiredException
        # load test scenario
        if self.requirements_file:
            self.test_scenario = ScenarioIOManager.load_test_scenario(self.requirements_file)
        elif self.requirements_dict:
            self.test_scenario = self.requirements_dict
        # test generation
        test_generation = TestGeneration(self.test_scenario)
        self.prompts = test_generation.generate_scenario(PromptIOManager.load_prompts(self.__prompts_path))
        # aux: for output reasons
        self.__update_figures(test_generation)
        self.__current_status = StateMachineKind.generated
    
    def execute(self):
        if (self.__current_status != StateMachineKind.generated): raise WrongStateException
        time_ini = datetime.now()
        # test execution
        test_execution = TestExecution(self.test_scenario, self.prompts, self.__api_keys)
        test_execution.execute_scenario()
        time_end = datetime.now()
        print(f'Time elapsed for executing {self.__num_instances} instances (from {self.__num_prompts} prompt templates): ' + str(time_end - time_ini))
        self.__current_status = StateMachineKind.executed
    
    def evaluate(self):
        if (self.__current_status != StateMachineKind.executed): raise WrongStateException
        time_ini = datetime.now()
        # test evaluation
        test_evaluation = TestEvaluation(test_id=self.test_scenario.test_id,
                                         prompts=self.prompts,
                                         requirements=self.test_scenario.ethical_requirements,
                                         perform_generic_evaluations=self.test_scenario.perform_generic_evaluations,
                                         perform_post_reasoning=self.test_scenario.perform_post_reasoning,
                                         api_keys=self.__api_keys)
        test_evaluation.execute_evaluation()
        time_end = datetime.now()
        print(f'Time elapsed for evaluating {self.__num_instances} instances (from {self.__num_prompts} prompt templates): ' + str(time_end - time_ini))
        self.__current_status = StateMachineKind.evaluated

    def report(self):
        if (self.__current_status != StateMachineKind.evaluated): raise WrongStateException
        reporting = ReportingManager()
        reporting.generate_report(self.test_scenario.test_id, self.prompts, self.test_scenario.perform_generic_evaluations, self.__save_generated_images)
