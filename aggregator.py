import os

from config import AggregationConfig
from file_system_utils import FileSystemUtils

class Aggregator:
    def __init__(self, aggregation_configs: list[AggregationConfig]):
        self.aggregation_configs = aggregation_configs
    
    def aggregate_text_files(self) -> None:
        """Combines all .txt files in a directory into a single file with each file's name and contents."""
        print("Aggregating files...")
        
        for agg in self.aggregation_configs:
            with open(agg.output_filepath, "w", encoding="utf-8") as outfile:
                for filename in FileSystemUtils.list_text_files_by_name_asc(agg.input_directory):
                    input_filepath = os.path.join(agg.input_directory, filename)
                    
                    if os.path.isfile(input_filepath) and filename.endswith(".txt"):
                        with open(input_filepath, "r", encoding="utf-8") as infile:
                            outfile.write(f"--- {filename} ---\n")
                            outfile.write(infile.read())
                            outfile.write("\n\n")

            print(f"All .txt files combined into {agg.output_filepath}")
