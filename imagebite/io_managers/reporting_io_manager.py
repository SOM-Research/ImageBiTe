from pathlib import Path
import pandas

GENERIC_VALIDATIONS_FILENAME = 'generic_validations'
CONCRETE_VALIDATIONS_FILENAME = 'concrete_validations'
    
def write_output_file(test_id, dataframe: pandas.DataFrame, filename):
    path = f'outputs/{test_id}'
    filename = f'{filename}.csv'
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(p / filename)