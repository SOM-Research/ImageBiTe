import pandas
from imagebite.model.prompt import Prompt
import numpy as np


def load_prompts(prompts_path):
    all_prompts = []
    # reads a csv file containing the prompts, with the following columns:
    # - 0: prompt id
    # - 1: discrimination: stereotyping, under-representation, denigration, ex-nomination
    # - 2: ethical concern: gender, age, ethnicity, religion/belief, disability, sexual orientation, political orientation
    # - 3: prompt template
    prompts_df = pandas.read_csv(prompts_path, sep='\t')
    prompts_df = prompts_df.replace({np.nan: None})
    for value in prompts_df.values.tolist():
        prompt = Prompt(id=value[0],
                        target_discriminations=value[1],
                        target_ethical_concerns=value[2],
                        template=value[3],
                        ethical_concern=value[4],
                        dimension=value[5])
        all_prompts.append(prompt)
    return all_prompts