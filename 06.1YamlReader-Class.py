import importlib
from multiprocessing import Queue

import yaml


class YamlPipelineExecutor:
    def __init__(self, pipeline_location):
        self._pipeline_location= pipeline_location
        self._queues = {}
        self._workers = {}

    def _load_pipeline(self):
        with open(self._pipeline_location) as f:
            self._yaml_data = yaml.safe_load(f)

    def _initialize_queues(self):
        for queue in self._yaml_data["queues"]:
            self._queues[queue["name"]] = Queue()

    def _initialize_workers(self):
        for worker in self._yaml_data["workers"]:
            WorkerClass = getattr(importlib.import_module(worker["location"]), worker["class"])
            input_queue = worker.get("input_queue")
            output_queues = worker.get("output_queue")
            instances = worker.get("instances", 1)

            init_params = {
                "input_queue": self._queue[input_queue] if input_queue is not None else None,
                "output_queue": [self._queues[output_queue] for output_queue in output_queues if output_queue is not None]
            }

            for i in range(instances):
                self._workers[worker["name"]].append(WorkerClass(**init_params))

    def process_pipelien(self):
        self._load_pipeline()
        self._initialize_queues()
