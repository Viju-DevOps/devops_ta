import yaml
import pkg_resources


def get_configurations():
    with open(pkg_resources.resource_filename('configuration', 'configuration.yaml'), 'r') as file:
        configurations = yaml.safe_load(file)
    return configurations
