import re

def normalize_and_case_string(input: str, to_lower: bool = True, to_upper: bool = False) -> str:
    result = input.strip().replace('\'','').replace('"','').replace('.','')
    if to_lower: return result.lower()
    if to_upper: return result.upper()
    return result

def clean_json_string(input: str):
    input = input.replace('```', '')
    input = re.sub('\n',' ',input.strip()).lower()
    match = re.search(r'\[.*?\]', input, re.DOTALL)
    return match.group()