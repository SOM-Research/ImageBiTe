from imagebite.t2i_services.t2i_abstract_factory import T2IFactory
from imagebite.validators.concrete_validator import ConcreteValidatorServiceBuilder


validator_factory = T2IFactory()
#validator_factory.register_builder('stereotyping', StereotypingValidatorServiceBuilder())
validator_factory.register_builder('underrepresentation', ConcreteValidatorServiceBuilder())
