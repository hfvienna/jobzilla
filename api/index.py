import os
import json

from flask import Flask
app = Flask(__name__)

def load_job_data(directory):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r') as f:
                job = json.load(f)
                data.append(job)
    return data

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    data = load_job_data('root/public/jobs/JSONs')  # Load job data
    df = pd.DataFrame(data)  # Convert list of dicts to DataFrame
    df_sorted = df.sort_values('fit', ascending=False)  # Sort by fit
    return df_sorted.to_json(orient='records')  # Convert DataFrame back to JSON

if __name__ == '__main__':
  app.run(port=5328)
