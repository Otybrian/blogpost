# from .main import app
import urllib.request,json


def get_quotes():

    quotes_list=[]

    get_quotes_url = 'http://quotes.stormconsultancy.co.uk/random.json'
    with urllib.request.urlopen(get_quotes_url) as url:
        get_quotes_data = url.read()
        get_quotes_response=json.loads(get_quotes_data)
        id= str(get_quotes_response['id'])
        quote=str(get_quotes_response['quote'])
        author=str(get_quotes_response['author'])
        
        new_list=[id,quote,author]
        quotes_list.append(new_list)
        
    return quotes_list[0]
    
