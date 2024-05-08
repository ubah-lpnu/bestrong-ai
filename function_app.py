import azure.functions as func
import logging
import os
from azure.storage.fileshare import ShareFileClient
from azure.storage.blob import BlobServiceClient, BlobClient, ContentSettings

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


connection_string = os.getenv("STORAGE_ACCOUNT_CONNECTION_STRING")

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    pdf_file_name = req.params.get('file_name')

    if not pdf_file_name:
        return func.HttpResponse(
            "Please provide the name of the PDF file in the query parameter 'file_name'.",
            status_code=400
        )

    try:
        file_share_name = "fsbestrongpdf"
        file_client = ShareFileClient.from_connection_string(
            conn_str=connection_string,
            share_name=file_share_name,  
            file_path=pdf_file_name
        )

        with open(pdf_file_name, "wb") as file:
            download = file_client.download_file()
            file.write(download.readall())

        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_name = "bestrong-data"
        container_client = blob_service_client.get_container_client(container_name)


        # blob_client = blob_service_client.get_blob_client(container=container_name, blob=pdf_file_name)
        with open(pdf_file_name, "rb") as file:
            container_client.upload_blob(pdf_file_name, 
                                         file, 
                                         overwrite=True,
                                         content_settings=ContentSettings(content_type="application/pdf"))
            # container_client.upload_blob(file, 
            #                         overwrite=True, 
            #                         content_settings=ContentSettings(content_type="application/pdf"))

        

        return func.HttpResponse("PDF file uploaded to Azure Blob Storage successfully.", status_code=200)


        # with open(pdf_file_name, "wb") as file:
        #     download = file_client.download_file()
        #     file.write(download.readall())

        # with open(pdf_file_name, "rb") as file:
        #     pdf_content = file.read()
        #     return func.HttpResponse(pdf_content, mimetype="application/pdf")
        
        os.remove(pdf_file_name)

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return func.HttpResponse(
            f"An error occurred while processing the request: {str(e)}",
            status_code=500
        )
