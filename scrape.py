import os
from langchain_community.document_loaders import RecursiveUrlLoader
from bs4 import BeautifulSoup as Soup
import requests
from dotenv import load_dotenv
load_dotenv()

# os.environ["HTTP_PROXY"] = os.getenv("HTTP_PROXY")
# os.environ["HTTPS_PROXY"] = os.getenv("HTTPS_PROXY")

def main():
    def test_access():
        try:
            check = requests.get(
                "https://www.cet.edu.in/noticefiles/271_AI%20Lect%20Notes.pdf",
                headers={"User-Agent": os.environ.get("USER_AGENT")},
                timeout=10
            )
            return True
        except Exception as e:
            return False

    if test_access():
        def simple_extractor(html: str) -> str:
            soup = Soup(html, "html.parser")
            return soup.get_text()
        
        try:
            loader = RecursiveUrlLoader(
                url="https://www.cet.edu.in/noticefiles/271_AI%20Lect%20Notes.pdf",
                max_depth=2, 
                timeout=30,
                extractor=simple_extractor,
                prevent_outside=True,
                check_response_status=True,
                use_async=False,
                continue_on_failure=True,
            )
            
            data = loader.load()
        
        except Exception as e:
            import traceback
            traceback.print_exc()
    return data

if __name__ == "__main__":
    main()