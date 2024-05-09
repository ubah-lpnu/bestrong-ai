import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import ContentFormat
import base64
import logging
import json

class DocumentAIHandler:
    def __init__(self):
        self.endpoint = os.getenv("DOCUMENTAI_ENDPOINT")
        self.key = os.getenv("DOCUMENTAI_KEY")

        self.document_intelligence_client = DocumentIntelligenceClient(
            endpoint=self.endpoint, 
            credential=AzureKeyCredential(self.key)
        )

    def analyze_document(self, pdf_file_name, output_json_path):
        with open(pdf_file_name, "rb") as file:
            file_content = file.read()

            analyze_request = {
                "base64Source": base64.b64encode(file_content).decode("utf-8")
            }
            
            poller = self.document_intelligence_client.begin_analyze_document(
                model_id="prebuilt-layout",
                analyze_request=analyze_request,
                output_content_format=ContentFormat.TEXT
            )
            result = poller.result()
            self.convert_to_json(result, output_json_path)
        
    def convert_to_json(self, result, output_json_path):
        result_json = result.as_dict()
        with open(output_json_path, "w") as output_file:
            json.dump(result_json, output_file, indent=4)
        logging.info(f"JSON output saved to {output_json_path}")
        
    



