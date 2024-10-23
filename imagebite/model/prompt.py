#from itertools import permutations
import re
from imagebite.t2i_services.t2i_service import T2IService
from imagebite.model.prompt_instance import PromptInstance

# -----------------------------------------------------------------------
# constants
# -----------------------------------------------------------------------

PROMPT_DELIMITER = f'"""'

MARKUP_START = '{'
MARKUP_END = '}'

# -----------------------------------------------------------------------
# main class
# -----------------------------------------------------------------------

class Prompt:

    @property
    def prompt_id(self):
        return self.__id
        
    @property
    def template(self) -> str:
        return self.__template
    
    @property
    def target_discriminations(self) -> list[str]:
        return self.__target_discriminations

    @target_discriminations.setter
    def target_discriminations(self, value: str):
        self.__target_discriminations = value.split(';')
    
    @property
    def target_ethical_concerns(self) -> list[str]:
        return self.__target_ethical_concerns
    
    @target_ethical_concerns.setter
    def target_ethical_concerns(self, value: str):
        self.__target_ethical_concerns = value.split(';')
    
    @property
    def ethical_concern(self):
        return self.__ethical_concern
    
    @property
    def dimension(self):
        return self.__dimension

    @property
    def instances(self) -> list[PromptInstance]:
        return self.__instances
        
    def __init__(self, id, target_discriminations, target_ethical_concerns, template, ethical_concern = None, dimension = None, **ignore):
        self.__id = id
        self.target_discriminations = target_discriminations
        self.target_ethical_concerns = target_ethical_concerns
        self.__template = template
        self.__ethical_concern = ethical_concern
        self.__dimension = dimension
    
    def instantiate(self, ethical_concerns, dimensions):
        # NOTE: so far, only one ethical concern max and/or one dimension max are considered
        # Improvement: allow many ethical concerns and many dimensions
        if ((self.ethical_concern is None) and (self.dimension is None)):
            self.__instances = [PromptInstance(0, self.template)]
        else:
            self.__generate_many_instances(ethical_concerns, dimensions)
    
    def execute(self, model: str, t2iservice: T2IService, num_samples = 1):
        prompt_instance: PromptInstance
        for prompt_instance in self.instances:
            i = num_samples
            while i >= 1:
                response = t2iservice.execute_prompt(prompt_instance.instance)
                response.model = model
                prompt_instance.add_response(response)
                i -= 1


    # -----------------------------------------------------------------------
    # auxiliary methods
    # -----------------------------------------------------------------------

    def __generate_many_instances(self, ethical_concerns, dimensions):
        ethical_concern = next(iter([ec for ec in ethical_concerns if ec['ethical_concern'] == self.ethical_concern]), None)
        dimension = next(iter([d for d in dimensions if d['type'] == self.dimension]), None)
        instances = [{'text': self.template, 'sensitive_communities': [], 'dimensions': []}]
        if ethical_concern is not None:
            instances = self.__generate_instances(instances, self.ethical_concern, ethical_concern['markup'], ethical_concern['sensitive_communities'], 'sensitive_communities')
        if dimension is not None:
            instances = self.__generate_instances(instances, self.dimension, 'DIMENSION', dimension['values'], 'dimensions')
        prompt_instances = [PromptInstance(instance_id=idx,
                                           instance=i['text'],
                                           sensitive_communities=i['sensitive_communities'],
                                           dimensions=i['dimensions'])
                            for idx, i in enumerate(instances)]
        self.__instances = prompt_instances

    def __generate_instances(self, instantiable_templates: list, prompt_characteristic, characteristic_markup, characteristic_values, characteristic_collection_key):
        if ((prompt_characteristic is not None) and (len(characteristic_values) > 0)):
            return self.__replace_markups(instantiable_templates, characteristic_markup, characteristic_values, characteristic_collection_key)
        else:
            return instantiable_templates
    
    # def __generate_dimension_instances(self, instances: list, dimension, dimension_definition):
    #     if ((dimension is not None) and (len(dimension_definition['values']) > 0)):
    #         return self.__replace_markups(instances, 'DIMENSION', dimension_definition['values'], 'dimensions')
    #     else:
    #         return instances

    def __replace_markups(self, instantiable_templates, markup_root, characteristic_values, characteristic_collection_key):
        instances = []
        for template in instantiable_templates:
            # define a regular expression pattern to match content within curly brackets
            # and find all distinct markups in the template
            pattern = re.compile(f'{MARKUP_START}{markup_root}[0-9]*?{MARKUP_END}')
            markups = set(pattern.findall(template['text']))
            for markup in markups:
                for characteristic in characteristic_values:
                    instance = template.copy()
                    instance['text'] = instance['text'].replace(markup, characteristic)
                    instance[characteristic_collection_key] = [characteristic]
                    instances.append(instance)
        return instances
    
    # def __replace_markups(self, instantiable_templates, markup_root, communities):
    #     instances = []
    #     for template in instantiable_templates:
    #         # define a regular expression pattern to match content within curly brackets
    #         # and find all distinct markups in the template
    #         pattern = re.compile(f'{MARKUP_START}{markup_root}[0-9]*?{MARKUP_END}')
    #         markups = set(pattern.findall(template))

    #         # generate all combinations of communities according to number of markups
    #         # excluding combinations comparing a community to itself
    #         communities_combos = [combo for combo in permutations(communities, len(markups)) if len(set(combo)) == len(combo)]

    #         for combo in communities_combos:
    #             instantiated_prompt = template
    #             communities = []
    #             for markup, community in zip(markups, combo):
    #                 instantiated_prompt = instantiated_prompt.replace(markup, community)
    #                 communities.append(community)
    #             #instance = PromptInstance(instantiated_prompt)
    #             #instance.add_communities(communities)
    #             instances.append(instantiated_prompt)

    #     return instances