from dotenv import load_dotenv
import os

def load_api_keys():
    load_dotenv()
    __config = {
        'openai_api_key' : os.environ["API_KEY_OPENAI"],
        'huggingface_api_key' : os.environ["API_KEY_HUGGINGFACE"],
        'replicate_api_key': os.environ["API_KEY_REPLICATE"]
    }
    return __config

def load_github_keys():
    load_dotenv()
    __config = {
        'github_repo' : os.environ['GITHUB_REPO'],
        'github_repo_prefix' : os.environ['GITHUB_REPO_PREFIX'],
        'github_token' : os.environ['GITHUB_TOKEN']
    }
    return __config