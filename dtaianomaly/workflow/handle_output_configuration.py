
import os
import json
from typing import Dict, Any, Union, Optional, Tuple

PlainOutputConfiguration = Union[Dict[str, Dict[str, Any]], str]


class OutputConfiguration:
    """
    The output configuration.
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    # The directory where everything should be saved
    directory_path: str
    algorithm_name: str

    # Whether the different intermediate information should be printed or not
    verbose: bool = False

    # Basic algorithm properties
    trace_time: bool = False
    trace_memory: bool = False

    # If the raw results should be saved as a file
    print_results: bool = False
    save_results: bool = False
    constantly_save_results: bool = False
    results_file: str = 'results.csv'

    # If a figure of the anomaly scores should be saved
    save_anomaly_scores_plot: bool = False
    anomaly_scores_plots_directory: str = 'anomaly_score_plots'
    anomaly_scores_plots_file_format: str = 'svg'
    anomaly_scores_plots_show_anomaly_scores: str = 'overlay'
    anomaly_scores_plots_show_ground_truth: Optional[str] = None

    # If the raw anomaly scores should be saved or not
    save_anomaly_scores: bool = False
    anomaly_scores_directory: str = 'anomaly_scores'

    # Raise an error of the train type of the algorithm does not match the train type of the dataset
    invalid_train_type_raise_error: bool = True

    @property
    def directory(self) -> str:
        return f'{self.directory_path}/{self.algorithm_name}'

    @property
    def results_path(self) -> str:
        return f'{self.directory}/{self.results_file}'

    def intermediate_results_path(self, dataset_index: Tuple[str, str]) -> str:
        return f'{self.directory}/tmp_intermediate_results_{self.dataset_index_to_str(dataset_index)}.csv'

    @property
    def anomaly_score_plots_directory_path(self) -> str:
        return f'{self.directory}/{self.anomaly_scores_plots_directory}'

    def anomaly_score_plot_path(self, dataset_index: Tuple[str, str]) -> str:
        return f'{self.anomaly_score_plots_directory_path}/{self.dataset_index_to_str(dataset_index)}.{self.anomaly_scores_plots_file_format}'

    @property
    def anomaly_scores_directory_path(self) -> str:
        return f'{self.directory}/{self.anomaly_scores_directory}'

    def anomaly_scores_path(self, dataset_index: Tuple[str, str]) -> str:
        return f'{self.anomaly_scores_directory_path}/{self.dataset_index_to_str(dataset_index)}'

    @staticmethod
    def dataset_index_to_str(dataset_index: Tuple[str, str]) -> str:
        return f'{dataset_index[0].lower()}_{dataset_index[1].lower()}'


def handle_output_configuration(plain_output_configuration: Union[PlainOutputConfiguration, OutputConfiguration], algorithm_name: str) -> OutputConfiguration:

    # If a proper output configuration is already given, then use that one
    if type(plain_output_configuration) is OutputConfiguration:
        output_configuration = plain_output_configuration

    # Otherwise, convert the json file or the plain configuration to an output configuration
    else:
        if type(plain_output_configuration) is str:
            configuration_file = open(plain_output_configuration, 'r')
            plain_output_configuration = json.load(configuration_file)
            configuration_file.close()

        output_configuration = OutputConfiguration(**plain_output_configuration, algorithm_name=algorithm_name)

    # Create the directory if it does not exist yet
    os.makedirs(output_configuration.directory, exist_ok=True)

    # Create a directory for the anomaly score plots, if they should be saved
    if output_configuration.save_anomaly_scores_plot and not os.path.exists(output_configuration.anomaly_score_plots_directory_path):
        os.mkdir(output_configuration.anomaly_score_plots_directory_path)

    # Create a directory for the anomaly scores, if they should be saved
    if output_configuration.save_anomaly_scores and not os.path.exists(output_configuration.anomaly_scores_directory_path):
        os.mkdir(output_configuration.anomaly_scores_directory_path)

    return output_configuration
