"""
YAML Pipeline Configuration Reader

This module reads and displays a YAML pipeline configuration file
as formatted JSON for inspection.

Purpose:
    - Demonstrate YAML parsing with PyYAML
    - Show pipeline configuration structure
    - Debug/visualize pipeline definitions

Configuration File:
    pipelines/wiki_yahoo_scraper_pipeline.yaml
"""

import json
import yaml


def main() -> None:
    """Load and print pipeline configuration as formatted JSON."""
    with open("./pipelines/wiki_yahoo_scraper_pipeline.yaml", "r") as f:
        yaml_data = yaml.safe_load(f)

    print(json.dumps(yaml_data, indent=4))


if __name__ == "__main__":
    main()