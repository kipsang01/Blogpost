import urllib.request,json
from config import Config
from .models import Quote


QUOTE_API = Config.QUOTE_API
def get_quotes():
    
    with urllib.request.urlopen(QUOTE_API) as url:
        get_quotes_data = url.read()
        get_quotes_response = json.loads(get_quotes_data)

        if get_quotes_response:
            author = get_quotes_response['author']
            quote = get_quotes_response['quote']
            link =get_quotes_response['permalink']
        new_quote = Quote(author, quote,link)
    return new_quote
