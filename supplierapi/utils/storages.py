from storages.backends.azure_storage import AzureStorage
from config.settings.base import env


class AzureMediaStorage(AzureStorage):
    account_name = env.str('AZURE_STORAGE_NAME')
    account_key = env.str('AZURE_STORAGE_KEY')
    azure_container = env.str('AZURE_STORAGE_MEDIA_CONTAINER')
    expiration_secs = None
