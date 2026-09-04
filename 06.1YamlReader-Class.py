"""
YAML Pipeline Executor

This module provides a class-based framework for executing
data pipelines defined in YAML configuration files.

Architecture:
    - YamlPipelineExecutor: Main orchestrator class
    - Dynamic worker loading via importlib
    - Queue-based communication between pipeline stages
    - Configurable worker instances per stage

Pipeline Definition (YAML):
    queues: List of named queues for inter-worker communication
    workers: List of worker definitions with:
        - name: Unique identifier
        - location: Python module path (e.g., Workers.WikiWorker)
        - class: Class name within module
        - instances: Number of parallel instances
        - input_queue: Queue name for input (optional)
        - output_queue: List of queue names for output (optional)

Purpose:
    - Demonstrate configuration-driven pipeline execution
    - Show dynamic class loading and instantiation
    - Implement producer-consumer pattern with multiprocessing queues

Note: This is a partial implementation - process_pipeline() is incomplete.
"""

import importlib
from multiprocessing import Queue

import yaml


class YamlPipelineExecutor:
    """
    Executes data processing pipelines defined in YAML configuration.

    Attributes:
        _pipeline_location: Path to YAML pipeline definition file.
        _queues: Dictionary mapping queue names to multiprocessing.Queue instances.
        _workers: Dictionary mapping worker names to lists of worker instances.
    """

    def __init__(self, pipeline_location: str) -> None:
        """
        Initialize the pipeline executor.

        Args:
            pipeline_location: Path to the YAML pipeline configuration file.
        """
        self._pipeline_location = pipeline_location
        self._queues = {}
        self._workers = {}

    def _load_pipeline(self) -> None:
        """Load and parse the YAML pipeline configuration."""
        with open(self._pipeline_location) as f:
            self._yaml_data = yaml.safe_load(f)

    def _initialize_queues(self) -> None:
        """Create multiprocessing queues for each queue defined in the pipeline."""
        for queue in self._yaml_data["queues"]:
            self._queues[queue["name"]] = Queue()

    def _initialize_workers(self) -> None:
        """
        Dynamically load and instantiate worker classes.

        For each worker definition:
        1. Import the module and get the class
        2. Resolve input/output queue references
        3. Create specified number of instances
        4. Store in _workers dictionary
        """
        for worker in self._yaml_data["workers"]:
            # Dynamic import: module.Class
            worker_module = importlib.import_module(worker["location"])
            WorkerClass = getattr(worker_module, worker["class"])

            input_queue_name = worker.get("input_queue")
            output_queue_names = worker.get("output_queue", [])
            instances = worker.get("instances", 1)

            # Resolve queue objects
            init_params = {
                "input_queue": self._queues[input_queue_name] if input_queue_name else None,
                "output_queue": [
                    self._queues[output_queue]
                    for output_queue in output_queue_names
                    if output_queue
                ]
            }

            # Create worker instances
            self._workers[worker["name"]] = []
            for _ in range(instances):
                self._workers[worker["name"]].append(WorkerClass(**init_params))

    def process_pipeline(self) -> None:
        """
        Execute the complete pipeline.

        Steps:
        1. Load pipeline configuration
        2. Initialize queues
        3. Initialize workers (incomplete - needs start/join logic)
        """
        self._load_pipeline()
        self._initialize_queues()
        self._initialize_workers()
        # TODO: Start workers, handle completion, cleanup


if __name__ == "__main__":
    # Example usage (when complete)
    # executor = YamlPipelineExecutor("./pipelines/wiki_yahoo_scraper_pipeline.yaml")
    # executor.process_pipeline()
    pass