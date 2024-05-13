import os
from azure.storage.fileshare import ShareFileClient
from azure.storage.blob import BlobServiceClient, ContentSettings
from azure.storage.fileshare import ShareServiceClient
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

        download_stream = file_client.download_file()
        pdf = download_stream.readall()
        return pdf
    
    def download_latest_file_from_share(self, file_share_name):
        service_client = ShareServiceClient.from_connection_string(conn_str=self.connection_string)
        share_client = service_client.get_share_client(file_share_name)
        file_list = list(share_client.list_directories_and_files())

        file_list.sort(key=lambda file: file['file_id'])

        latest_file = file_list[0]
        file_client = share_client.get_file_client(latest_file['name'])

        download = file_client.download_file()
        file = download.readall()

        return file, latest_file['name']

    def upload_file_to_blob(self, file, output_json):
       
        container_client = self.blob_service_client.get_container_client(self.container_name)
        container_client.upload_blob(
            name=output_json,
            data=file,
            overwrite=True,
            content_settings=ContentSettings(content_type="application/json")
        )
        logging.info(f"File uploaded to Azure Blob Storage successfully.")

    def delete_local_files(self, *args):
        for file in args:
            os.remove(file)
        logging.info("Local files deleted successfully.")