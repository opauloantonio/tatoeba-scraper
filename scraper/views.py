import logging
import requests
from bs4 import BeautifulSoup

from rest_framework.response import Response
from rest_framework.decorators import api_view


null = None
false = False
true = True


def get_sentence(source):
    # The next two lines are absolutely the most horrible lines I've written in five years!

    direct = [{**t, "direct": True} for t in [{k: sentence[k] for k in ('text', 'id', 'lang')} for sentence in source[1]]]
    indirect = [{**t, "direct": False} for t in [{k: sentence[k] for k in ('text', 'id', 'lang')} for sentence in source[2]]]
    
    return {
        "translations": direct + indirect,
        "text": source[0]['text'],
        "lang": source[0]['lang'],
        "id": source[0]['id'],
    }


@api_view(['POST'])
def search(request):
    page = requests.get(request.data['url'])

    soup = BeautifulSoup(page.text, features="html.parser")
    results = soup.find_all("h2")[0].text

    response = {
        'numberOfResults': results,
        'data': []
    }

    containers = soup.find_all("div", class_="sentence-and-translations")

    for c in containers:
        response['data'].append(get_sentence(eval(c.get("ng-init")[12:-1])))
        
    return Response(response, page.status_code)


@api_view(['POST'])
def sentence_details(request):
    try:
        page = requests.get(request.data['url'])

        soup = BeautifulSoup(page.text, features='html.parser')

        container = soup.find("div", class_="sentence-and-translations")
        
        return Response(get_sentence(eval(container.get("ng-init")[12:-1])), page.status_code)
    except Exception as e:
        print(e)
        return Response(status=500)


@api_view(['GET'])
def languages(request):
    user_language = request.GET.get("user_language")
    
    if user_language == None:
        user_language = "eng"

    url = f"https://tatoeba.org/{user_language}/stats/sentences_by_language"

    page = requests.get(url)
    soup = BeautifulSoup(page.text, features='html.parser')

    languages_table = soup.find("table", class_="languages-stats")

    languages_list = []

    for i, tr in enumerate(languages_table):
        try:
            img = tr.contents[1].find("img")

            languages_list.append({
                "img": f"https://tatoeba.org{img.get('src')}",
                "language": img.get('title'),
                "code": img.get("alt"),
            })
        except:
            pass

    return Response(languages_list, status=200)