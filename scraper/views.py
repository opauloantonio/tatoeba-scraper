import logging
import requests
from bs4 import BeautifulSoup

from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['POST'])
def search(request):
    try:
        page = requests.get(request.data['url'])

        soup = BeautifulSoup(page.text, features="html.parser")

        results = soup.find_all("h2")[0].text.split()[-2]

        if len(results) == 0:
            return Response({'data': [], 'numberOfResults': 0}, page.status_code)

        response = {
            'numberOfResults': results,
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

            sentence = container.find_all(class_='sentence')[0]

            response['data'].append({
                'text': sentence.find('div', class_='text').text.strip(),
                'language': sentence.find('img').get('alt'),
                'id': sentence.find_all(class_="md-icon-button")[-1].get("href")[20::],
                'translations': translations
            })
            
        return Response(response, page.status_code)
    except Exception as e:
        #print(e)
        logging.exception(e)
        return Response(status=500)


@api_view(['POST'])
def sentence_details(request):
    try:
        page = requests.get(request.data['url'])
        soup = BeautifulSoup(page.text, features='html.parser')
        
        translations = []

        for t in soup.find_all(class_='translation'):
            translations.append({
                'text': t.find('div', class_='text').text.strip(),
                'language': t.find('img').get('alt'),
                'id': t.find_all(class_="md-icon-button")[-1].get("href")[20::],
                "direct": 'direct' in t.find_parent("div").get("class")
            })

        sentence = soup.find_all(class_='sentence')[0]

        data = {
            'text': sentence.find('div', class_='text').text.strip(),
            'language': sentence.find('img').get('alt'),
            'id': sentence.find_all(class_="md-icon-button")[-1].get("href")[20::],
            'translations': translations
        }
        
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