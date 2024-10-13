import requests
import PyPDF2
from gentopia.tools.basetool import *

class PDFReaderArgs(BaseModel):
    pdf_url: str = Field(..., description="The URL of the PDF file")

class PDFReader(BaseTool):
    name = "pdf_reader"
    description = "Fetches and reads a PDF file from a provided URL and returns its textual content"

    args_schema: Optional[Type[BaseModel]] = PDFReaderArgs

    def _run(self, pdf_url: str) -> str:
        try:
            # to send the request for downloading the PDF from the URL provided
            headers = {
                "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                               "AppleWebKit/537.36 (KHTML, like Gecko) "
                               "Chrome/91.0.4472.124 Safari/537.36")
            }
            response = requests.get(pdf_url, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            # for saving the downloaded PDF to a temp file
            with open("temp_downloaded.pdf", 'wb') as temp_pdf:
                temp_pdf.write(response.content)

            # for opening and reading the temp pdf file
            with open("temp_downloaded.pdf", 'rb') as temp_pdf_file:
                reader = PyPDF2.PdfReader(temp_pdf_file)
                extracted_text = ""
                # doing this to extract text from each page of the PDF provided
                for page in reader.pages:
                    extracted_text += page.extract_text()
                    
                # this is for returning a summary of the extracted text (first 4500 characters)
                return extracted_text[:450] + "..."
        
        except Exception as error:
            return f"Error occurred while processing the PDF: {str(error)}"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


