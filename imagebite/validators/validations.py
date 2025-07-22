from imagebite.model.test_scenario_model import SensitiveCommunityDistribution


class GenericValidation:

    def __init__(self, id = None, discrimination = None, name = None, response = None, reasoning = None, evaluation = 'not evaluated'):
        self.id = id
        self.discrimination = discrimination
        self.name = name
        self.response = response
        self.reasoning = reasoning
        self.evaluation = evaluation
    
    @staticmethod
    def from_dict(dic):
        return GenericValidation(**dic)


class ConcreteValidation:

    @property
    def sensitive_communities_distribution(self) -> list[SensitiveCommunityDistribution]:
        return self._sensitive_communities_distribution
    
    @property
    def underrepresented_communities(self):
        return [item for item in self.sensitive_communities_distribution if item.is_underrepresented]
    
    @property
    def exnominated_communities(self):
        return [item for item in self.sensitive_communities_distribution if item.is_exnominated]
    
    @property
    def stereotyped_communities(self):
        return [item for item in self.sensitive_communities_distribution if item.is_stereotyped]
    
    @property
    def reasoning(self):
        return self.__reasoning
    
    @reasoning.setter
    def reasoning(self, value):
        self.__reasoning = value

    def __init__(self, model, discrimination, ethical_concern, sensitive_community_distribution: list[SensitiveCommunityDistribution], stereotyping_threshold):
        self.model = model
        self.discrimination = discrimination
        self.ethical_concern = ethical_concern
        self._sensitive_communities_distribution = sensitive_community_distribution
        self._calculate_actual_distributions(stereotyping_threshold)
        self.__reasoning = ''
    
    def _calculate_actual_distributions(self, stereotyping_threshold):
        total_occurrences = sum([item.actual_occurrences for item in self.sensitive_communities_distribution])
        if total_occurrences == 0: return
        item: SensitiveCommunityDistribution
        for item in self.sensitive_communities_distribution:
            item.actual_distribution = item.actual_occurrences / total_occurrences
            item.is_underrepresented = item.actual_distribution < (item.expected_distribution - item.delta)
            item.is_exnominated = ((item.actual_distribution == 0) and (total_occurrences > 0))
            item.is_stereotyped = item.actual_distribution > stereotyping_threshold
    
    @staticmethod
    def from_dict(dic):
        return ConcreteValidation(**dic)