from .settings import get_model_env



def get_config():
    """
    Returns configuration settings.

    Return parameters:
    - isServer (bool): Indicates if the server configuration is enabled.
    - isLocal (bool): Indicates if the local configuration is enabled.
    - apikey (str): The API key for the enabled configuration.
    - domainname (str): The domain name for the enabled configuration.
    - modelname (str): The model name for the enabled configuration.
    - temperature (float): The temperature setting for the model.
    - system_prompt (str): The system prompt content.
    """
    try:
        settings = get_model_env()
    except Exception as e:
        settings = {
            "isServer": False,
            "isLocal": False,
            "apikey": "",
            "domainname": "",
            "modelname": "",
            "temperature": 0.01,
            "system_prompt": ""
        }
    return settings

