import azure.functions as func
import logging
from storage_handler import StorageHandler
from document_ai_handler import DocumentAIHandler


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

file_share_name = "fsbestrongpdf"
container_name = "bestrong-data"

storage_handler = StorageHandler(file_share_name, container_name)
document_ai_handler = DocumentAIHandler()

@app.route(route="ai-document-analysis")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        pdf, file_name_pdf = storage_handler.download_latest_file_from_share(file_share_name)
        output_json = file_name_pdf.replace("pdf", "json")
        doc = document_ai_handler.analyze_document(pdf)
        storage_handler.upload_file_to_blob(doc, output_json)
        return func.HttpResponse("PDF file uploaded to Azure Blob Storage successfully.", status_code=200)

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return func.HttpResponse(
            f"An error occurred while processing the request: {str(e)}",
            status_code=500
        )