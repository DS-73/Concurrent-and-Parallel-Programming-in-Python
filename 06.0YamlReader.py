import json

import yaml

with open("./pipelines/wiki_yahoo_scraper_pipeline.yaml", "r") as f:
    yaml_data = yaml.safe_load(f)

print(json.dumps(yaml_data, indent=4))