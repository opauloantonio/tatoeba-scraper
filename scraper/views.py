import json
import requests
from bs4 import BeautifulSoup

from rest_framework.decorators import api_view

from django.http import HttpResponse


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
        'sentences': []
    }

    containers = soup.find_all("div", class_="sentence-and-translations")

    for c in containers:
        response['sentences'].append(get_sentence(eval(c.get("ng-init")[12:-1])))
        
    return HttpResponse(
        json.dumps(response),
        content_type='application/json',
    )


@api_view(['POST'])
def sentence_details(request):
    try:
        page = requests.get(request.data['url'])

        soup = BeautifulSoup(page.text, features='html.parser')

        container = soup.find("div", class_="sentence-and-translations")

        return HttpResponse(
            json.dumps(get_sentence(eval(container.get("ng-init")[12:-1]))),
            content_type='application/json',
        )

    except Exception as e:
        print(e)
        return HttpResponse(status=500)


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

    return HttpResponse(
        json.dumps(languages_list),
        content_type='application/json',
    )


@api_view(['GET'])
def get_random_sentence(request):
    language = request.GET.get("lang", "und")

    page = requests.get(
        "https://www.tatoeba.org/eng/sentences/random/" + language
    )

    soup = BeautifulSoup(page.text, features='html.parser')

    main_sentence = soup.find("div", class_="mainSentence")

    extract_sentence = lambda container : {
        "id": container.get("data-sentence-id"),
        "lang": container.find("div", class_="lang").find("img").get("alt"),
        "text": container.find("div", class_="text").text,
    }

    sentence = dict({
        'translations': [],
        **extract_sentence(main_sentence)
    })

    for t in soup.find_all("div", class_="directTranslation"):
        sentence['translations'].append(
            dict({"direct": True}, **extract_sentence(t))
        )

    for t in soup.find_all("div", class_="indirectTranslation"):
        sentence['translations'].append(
            dict({"direct": False}, **extract_sentence(t))
        )

    return HttpResponse(
        json.dumps(sentence),
        content_type='application/json',
    )
