from ..config import get_config


def get_endpoint(service):
    return get_config['api']['BASE_URL']
