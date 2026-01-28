import json
import urllib.request
import gzip
import re
from io import BytesIO
from html.parser import HTMLParser

MAX_SIZE = 500_000


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        clean = data.strip()
        if clean:
            self.text.append(clean)

    def get_text(self):
        return " ".join(self.text)


def extract_url(event):
    if isinstance(event, dict) and "url" in event:
        return event["url"]

    for param in event.get("parameters", []):
        if param.get("name") == "url":
            return param.get("value")

    text = event.get("inputText", "")
    match = re.search(r"https?://[^\s]+", text)
    if match:
        return match.group(0)

    return None


def fetch_url(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as response:
        raw = response.read(MAX_SIZE)

        if response.headers.get("Content-Encoding") == "gzip":
            buf = BytesIO(raw)
            raw = gzip.GzipFile(fileobj=buf).read(MAX_SIZE)

        return raw.decode("utf-8", errors="ignore")


def clean_html(html):
    parser = TextExtractor()
    parser.feed(html)
    return parser.get_text()


def lambda_handler(event, context):
    print("RAW EVENT:", json.dumps(event))

    try:
        url = extract_url(event)

        if not url:
            body = "No URL found in request. Please provide a valid URL."
        else:
            html = fetch_url(url)
            text = clean_html(html)
            body = f"Scraped content from {url}:\n\n{text[:5000]}"

        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": "web_scrape",
                "function": "web_scrape",
                "functionResponse": {
                    "responseBody": {
                        "TEXT": {
                            "body": body
                        }
                    }
                }
            }
        }

    except Exception as e:
        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": "web_scrape",
                "function": "web_scrape",
                "functionResponse": {
                    "responseBody": {
                        "TEXT": {
                            "body": f"Scraper error: {str(e)}"
                        }
                    }
                }
            }
        }
