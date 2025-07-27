from tools.base_tool import BaseTool

class WebScraperTool(BaseTool):

    name = "scrape"
    description = "Scrape and extract plain text from a website URL."
    parameters = {
        "type": "object",
        "properties": {
            "url": {"type": "string", "description": "A valid website URL (e.g. https://...)"}
        },
        "required": ["url"],
    }

    def run(self, **kwargs) -> str:
        import requests
        from bs4 import BeautifulSoup
        try:
            url=kwargs["url"]
            res = requests.get(url)
            soup = BeautifulSoup(res.text, "html.parser")
            return soup.get_text()[:1000]
        except Exception as e:
            return f"❌ Scraping error: {e}"