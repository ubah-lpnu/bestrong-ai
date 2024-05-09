import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

class DocumentAIHandler:
    def __init__(self):
        self.endpoint = os.getenv("DOCUMENTAI_ENDPOINT")
        self.key = os.getenv("DOCUMENTAI_KEY")

        self.document_intelligence_client = DocumentIntelligenceClient(
            endpoint=self.endpoint, 
            credential=AzureKeyCredential(self.key)
        )

    def analyze_document(self, pdf_file_name):
        with open(pdf_file_name, "rb") as file:
            poller = self.document_intelligence_client.begin_analyze_document("prebuilt-document", file)
            result = poller.result()
            return result



