from enum import Enum
from imagebite import utils
from datetime import datetime

DiscriminationKind = Enum('Discrimination', 'stereotyping underrepresentation')

class SensitiveCommunityDistribution:

    @property
    def as_string(self):
        return self.sensitive_community + ' (' + str(self.actual_occurrences) + ',{:6.2f}'.format(self.actual_distribution*100) + '%)'

    def __init__(self, sensitive_community: str, expected_distribution: float = 0.0, delta: float = 0.0):
        self.sensitive_community = utils.normalize_and_case_string(sensitive_community)
        self.expected_distribution = expected_distribution
        self.delta = delta
        self.actual_occurrences = 0
        self.actual_distribution = 0.0
        self.is_underrepresented = False
        self.is_exnominated = False
        self.is_stereotyped = False


class EthicalRequirement:

    @property
    def expected_distributions(self):
        return self.__expected_distributions

    def __init__(self, name, rationale, discrimination, ethical_concern, stereotyping_threshold = 0.0, **ignore):
        self.name = name
        self.rationale = rationale
        self.discrimination = discrimination
        self.ethical_concern = utils.normalize_and_case_string(ethical_concern)
        self.stereotyping_threshold = stereotyping_threshold
        self.__expected_distributions = []
    
    def add_expected_distribution(self, expected_distribution: SensitiveCommunityDistribution):
        self.__expected_distributions.append(expected_distribution)
        self.communities = [item.sensitive_community for item in self.__expected_distributions]
    
    def add_sensitive_communities(self, sensitive_communities: list[str]):
        self.__expected_distributions = [SensitiveCommunityDistribution(sc) for sc in sensitive_communities]
        self.communities = sensitive_communities


class TestScenario:

    @property
    def ethical_requirements(self):
        return self.__ethical_requirements

    def __init__(self, id, num_templates, num_samples, llms, dimensions, ethical_concerns, num_retries = 3, perform_generic_evaluations = False, perform_post_reasoning = False, **ignore):
        self.id = id
        timestamp = datetime.now()
        self.test_id = timestamp.strftime("%Y%m%d%H%M%S")
        self.num_templates = num_templates
        self.num_samples = num_samples
        self.num_retries = num_retries
        self.llms = llms
        self.perform_generic_evaluations = perform_generic_evaluations
        self.perform_post_reasoning = perform_post_reasoning
        self.__ethical_requirements = []
        self.dimensions = dimensions
        self.ethical_concerns = ethical_concerns
    
    def add_ethical_requirement(self, ethical_requirement: EthicalRequirement):
        self.__ethical_requirements.append(ethical_requirement)