import pandas
from pandas.core.common import flatten
from imagebite.reporting.concrete_validation_decorator import ConcreteValidationDecorator
from imagebite.reporting.generic_validation_decorator import GenericValidationDecorator
import imagebite.io_managers.image_io_manager as ImageIOManager
import imagebite.io_managers.reporting_io_manager as ReportingIOManager


class ReportingManager:

    def __init__(self):
        pass
        
    def generate_report(self, test_id, prompts: list, perform_generic_evaluations: bool = False, save_generated_images: bool = False):
        if len(prompts) == 0: return
        self.__test_id = test_id
        if perform_generic_evaluations:
            df = self.__report(prompts, self.__generate_generic_validation_report)
            self.__save_report(df, ReportingIOManager.GENERIC_VALIDATIONS_FILENAME)
        df = self.__report(prompts, self.__generate_concrete_validations_report)
        self.__save_report(df, ReportingIOManager.CONCRETE_VALIDATIONS_FILENAME)
        if (save_generated_images): self.__save_generated_images(prompts)

    # ----------------------------------------------------------------------------------------
    # Auxiliary methods for generating generic and concrete reports
    # ----------------------------------------------------------------------------------------

    def __generate_generic_validation_report(self, prompts: list):
        result = [GenericValidationDecorator(prompt).validations for prompt in prompts]
        return list(flatten(result))
    
    def __generate_concrete_validations_report(self, prompts: list):
        result = [ConcreteValidationDecorator(prompt).validations for prompt in prompts]
        return list(flatten(result))
    
    def __report(self, prompts, reporting_function):
        validations = reporting_function(prompts)
        validations_df = pandas.DataFrame.from_records([v.to_dict() for v in validations])
        print(validations_df)
        return validations_df
    
    # ----------------------------------------------------------------------------------------
    # Auxiliary methods for human-in-the-loop inspection
    # ----------------------------------------------------------------------------------------

    def __save_report(self, df, filename):
        ReportingIOManager.write_output_file(self.__test_id, df, filename)
    
    def __save_generated_images(self, prompts: list):
        print('saving images for human-in-the-loop inspection...')
        for prompt in prompts:
            for instance in prompt.instances:
                image_idx = 0
                for response in instance.responses:
                    ImageIOManager.save_or_download_image(self.__test_id,
                                          prompt_id=prompt.prompt_id,
                                          instance_id=instance.instance_id,
                                          model=response.model,
                                          image_idx=image_idx,
                                          image=response.response(),
                                          is_url=response.is_url())
                    image_idx += 1
        print('done')
