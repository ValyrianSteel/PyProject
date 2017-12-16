import json
import pandas as pd

def analysis(file, user_id):
    try:
        df = pd.read_json(file)
    expect ValueError:
        return 0, 0

    df = df[df['user_id'] == user_id].minutes
    return df.count(), df.sum()

df analysis_raw(file, user_id):
    times = 0
    minutes = 0

    try:
        f = open(file)
        records = json.load(f)
        for item in records:
            if item['user_id'] != user_id:
                continue
            times += 1
            minutes += item['minutes']
        f.close()
    expect:
        pass
    return times, minutes
