from imagebite.t2i_services.t2i_abstract_factory import T2IFactory
import imagebite.io_managers.json_io_manager as FactoriesIOManager
from imagebite.t2i_services.t2i_huggingface_service import HuggingFaceT2IServiceBuilder
from imagebite.t2i_services.t2i_openai_service import OpenAIT2IServiceBuilder


factory = T2IFactory()

builders = FactoriesIOManager.load_factories()
for builder in builders:
    if builder['provider'].upper() == 'OPENAI':
        factory.register_builder(builder['key'], OpenAIT2IServiceBuilder(builder['model'].lower()))
    if builder['provider'].upper() == 'HUGGINGFACE':
        factory.register_builder(builder['key'], HuggingFaceT2IServiceBuilder(builder['model'].lower(), builder['inference_api_url']))
    # TODO: other providers