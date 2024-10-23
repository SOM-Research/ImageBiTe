import imagebite.io_managers.file_manager as FileManager
from imagebite.model.test_scenario_model import DiscriminationKind, EthicalRequirement, SensitiveCommunityDistribution, TestScenario


def load_test_scenario(filename):
    # reads a json file containing the test scenario and
    # the ethical requirements model,
    # which are compliant with the grammar
    json_scenario = FileManager.load_json_from_file(filename)
    scenario = TestScenario(**json_scenario)
    requirements = json_scenario['requirements']
    for json_requirement in requirements:
        requirement = EthicalRequirement(**json_requirement)
        if requirement.discrimination == DiscriminationKind.underrepresentation.name:
            distributions = json_requirement['expected_distributions']
            for distribution in distributions:
                sensitive_community_distribution = SensitiveCommunityDistribution(**distribution)
                requirement.add_expected_distribution(sensitive_community_distribution)
        if requirement.discrimination == DiscriminationKind.stereotyping.name:
            requirement.add_sensitive_communities(json_requirement['sensitive_communities'])
        scenario.add_ethical_requirement(requirement)
    return scenario
    # TODO: pending validation against JSON schema

def load_factories():
    filename = FileManager.get_resource_path('factories.json')
    return FileManager.load_json_from_file(filename)
    # TODO: pending validation against JSON schema

def load_generic_validators():
    filename = FileManager.get_resource_path('generic_validators.json')
    return FileManager.load_json_from_file(filename)
    # TODO: pending validation against JSON schema