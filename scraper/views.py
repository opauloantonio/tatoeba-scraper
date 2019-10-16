import re
import requests
from bs4 import BeautifulSoup

from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['POST'])
def search(request):
    try:
        page = requests.get(request.data['url'])

        soup = BeautifulSoup(page.text, features="html.parser")

        results = re.findall('\d+', soup.find_all("h2")[1].text)

        if len(results) == 0:
            return Response({'data': [], 'numberOfResults': 0}, page.status_code)
        
        number_of_results = results[0] if len(results) == 1 else results[1]

        response = {
            'numberOfResults': number_of_results,
            'data': []
        }

        containers = soup.find_all("div", class_="sentence-and-translations")

        for container in containers:
            translations = []
            translationsContainers = container.findAll(class_="translation")

            for translation in translationsContainers:
                translations.append({
                    "text": translation.find(class_="text").text.strip(),
                    "language": translation.find(class_="lang").find("img").get('alt'),
                    "id": translation.find_all(class_="md-icon-button")[-1].get("href")[20::],
                    "direct": 'direct' in translation.find_parent("div").get("class")
                })
                
            response['data'].append({
                "text": container.find(class_="text").text.strip(),
                "language": container.find(class_="lang").find("img").get('alt'),
                "id": container.find_all(class_="md-icon-button")[-1].get("href")[20::],
                "translations": translations
            })
            
        return Response(response, page.status_code)
    except Exception as e:
        print(request.data['url'])
        print(e)
        return Response(status=500)


@api_view(['POST'])
def sentence_details(request):
    try:
        page = requests.get(request.data['url'])
        soup = BeautifulSoup(page.text, features='html.parser')

        data = []

        for x in soup.find_all(class_='sentence'):
           data.append({
               'text': x.find('div', class_='text').text,
               'language': x.find('img').get('alt'),
               'id': x.get('data-sentence-id'),
               'direct': 'directTranslation' in x.get('class')
            })
        
        return Response(data, page.status_code)
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