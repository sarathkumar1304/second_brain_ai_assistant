from pathlib import Path
import yaml

def load_yaml_file(file_path: Path):
    config = yaml.safe_load(file_path.read_text())
    config = config["parameters"]
    