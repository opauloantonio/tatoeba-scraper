import requests
from bs4 import BeautifulSoup

from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['POST'])
def scrap(request):
    try:
        page = requests.get(request.data['url'])

        soup = BeautifulSoup(page.text, features="html.parser")
        data = []

        containers = soup.find_all("div", class_="sentence-and-translations")

        for i, container in enumerate(containers):
            translations = []
            translationsContainers = container.findAll(class_="translation")

            for j, t in enumerate(translationsContainers):
                translations.append({
                    "text": t.find(class_="text").text.strip(),
                    "language": t.find(class_="lang").find("img").get('alt'),
                    "id": t.find("md-button").get("href")[20::],
                    "direct": 'direct' in t.find_parent("div").get("class")
                })
                
            data.append({
                "text": container.find(class_="text").text.strip(),
                "language": container.find(class_="lang").find("img").get('alt'),
                "id": container.find("md-button").get("href")[20::],
                "translations": translations
            })

            # TODO - add the links for the next and previous pages.

        return Response(data, status=page.status_code)
    except Exception as e:
        print(e)
        return Response(status=500)
