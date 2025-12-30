import numpy as np
import pandas as pd
from typing import Any

# Recursively convert numpy types to Python native types for JSON serialization. 
def convert_numpy_to_python(obj: Any) -> Any:
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {
            convert_numpy_to_python(k): convert_numpy_to_python(v) 
            for k, v in obj.items()
        }
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy_to_python(item) for item in obj]
    else:
        return obj

#Cleans geocoded city data
def clean_geocoded_data(data):
    if not data:
        return []
    df = pd.DataFrame(data)
    df = df.dropna(subset=['lat', 'lon'])
    df = df.drop_duplicates(subset=['name'])
    df = df.reset_index(drop=True)

    return df.to_dict('records')