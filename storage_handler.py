import os
from azure.storage.fileshare import ShareFileClient
from azure.storage.blob import BlobServiceClient, ContentSettings
import logging

class StorageHandler:
    def __init__(self, file_share_name, container_name):
        self.file_share_name = file_share_name
        self.container_name = container_name
        self.connection_string = os.getenv("STORAGE_ACCOUNT_CONNECTION_STRING")
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

    def download_file_from_share(self, file_share_name, file_name):
        file_client = ShareFileClient.from_connection_string(
            conn_str=self.connection_string,
            share_name=file_share_name,
            file_path=file_name
        )

        with open(file_name, "wb") as file:
            download = file_client.download_file()
            file.write(download.readall())
        return 

    def upload_file_to_blob(self, file_name):
       
        container_client = self.blob_service_client.get_container_client(self.container_name)
        with open(file_name, "rb") as file:
            container_client.upload_blob(
                name=file_name,
                data=file,
                overwrite=True,
                content_settings=ContentSettings(content_type="application/json")
            )
        logging.info(f"File uploaded to Azure Blob Storage successfully.")

    def delete_local_files(self, *args):
        for file in args:
            os.remove(file)
        logging.info("Local files deleted successfully.")