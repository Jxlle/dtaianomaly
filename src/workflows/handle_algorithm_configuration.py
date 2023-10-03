
import json
import importlib
from typing import Dict, Any, Union
from src.anomaly_detection import *

AlgorithmConfigurationType = Union[Dict[str, Any], str]


def handle_algorithm_configuration(algorithm_configuration: AlgorithmConfigurationType) -> TimeSeriesAnomalyDetector:

    # Read the algorithm configuration file if it is a string
    if type(algorithm_configuration) is str:
        configuration_file = open(algorithm_configuration, 'r')
        algorithm_configuration = json.load(configuration_file)
        configuration_file.close()

    # Load the specific anomaly detector class
    anomaly_detector_class_object: TimeSeriesAnomalyDetector = getattr(importlib.import_module('src.anomaly_detection'), algorithm_configuration['anomaly_detector'])

    # Load and return the specific anomaly detector instance
    return anomaly_detector_class_object.load(parameters=algorithm_configuration)
