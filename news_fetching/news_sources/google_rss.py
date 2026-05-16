import requests
from xml.etree import ElementTree

def fetch_google_rss(symbol: str, max_results: int = 5) -> list:
    """
    Fetches latest headlines for the given symbol from Google News RSS.
    
    Args:
        symbol (str): Stock/company name.
        max_results (int): Max number of headlines to return.

    Returns:
        List of dicts with 'title' and 'source'
    """
    url = f"https://news.google.com/rss/search?q={symbol}+stock&hl=en-IN&gl=IN&ceid=IN:en"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        root = ElementTree.fromstring(response.content)

        items = root.findall(".//item")
        results = []

        for item in items[:max_results]:
            title = item.findtext("title") or "No title"
            source = item.findtext("source") or "Google News"
            results.append({"title": title, "source": source})

        return results

    except Exception as e:
        print(f"[RSS Error] Failed to fetch news for {symbol}: {e}")
        return []
