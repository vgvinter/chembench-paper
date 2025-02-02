
import os
import json
import pickle
import pandas as pd

from chembench.analysis import (
    construct_name_to_path_dict,
)

from utils import obtain_chembench_repo
from paths import tex, data

def load_and_count(datafolder):
    data_paths = construct_name_to_path_dict(datafolder)

    paths = list(data_paths.values())

    data = []
    reasoning = 0
    knowledge = 0
    calculation = 0
    intuition = 0
    for path in paths:
        with open(path, "r") as file:
            data = json.load(file)
        keywords = data["keywords"]
        for keyword in keywords:
            if "requires" in keyword:
                if keyword == "requires-reasoning": 
                    reasoning += 1
                if keyword == "requires-knowledge":
                    knowledge += 1
                if keyword == "requires-calculation":
                    calculation += 1
                if keyword == "requires-intuition":
                    intuition += 1
                
    
    results = {
        "requires-reasoning": reasoning,
        "requires-knowledge": knowledge,
        "requires-calculation": calculation,
        "requires-intuition": intuition,
    }

    return results

if __name__ == "__main__":
    chembench_repo = obtain_chembench_repo()
    datafolder = os.path.join(
        chembench_repo, "data"
    )

    data = load_and_count(datafolder)

    # Save the data variable to a pickle file
    with open(os.path.join(data, 'requires_data.pkl'), 'wb') as f:
        pickle.dump(data, f)