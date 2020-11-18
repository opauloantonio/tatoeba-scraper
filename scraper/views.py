import json
import requests
from bs4 import BeautifulSoup

from rest_framework.decorators import api_view

from django.http import HttpResponse

from .utils import get_sentence_from_source, build_search_url_from_request_data


null = None
false = False
true = True


@api_view(['POST'])
def search(request):
    url = request.data.get("url") or build_search_url_from_request_data(request.data)

    if url is not None:
        page = requests.get(url)
    else:
        return HttpResponse(
            "You must either provide a full URL for a search page on Tatoeba or at least a text", 
            status=400,
            content_type='application/json',
        )

    soup = BeautifulSoup(page.text, features="html.parser")
    results = soup.find_all("h2")[0].text

    response = {
        'numberOfResults': results,
        'sentences': []
    }

    containers = soup.find_all("div", class_="sentence-and-translations")

    for c in containers:
        response['sentences'].append(get_sentence_from_source(eval(c.get("ng-init")[12:-1])))
        
    return HttpResponse(
        json.dumps(response),
        content_type='application/json',
    )


@api_view(['GET'])
def sentence_details(request, sentence_id):
    try:
        page = requests.get(
            "https://www.tatoeba.org/eng/sentences/show/" + sentence_id
        )

        soup = BeautifulSoup(page.text, features="html.parser")

        container = soup.find("div", class_="sentence-and-translations")

        data = {
            "sentence": get_sentence_from_source(eval(container.get("ng-init")[12:-1])),
            "comments": [],
        }

        comment_cards = soup.find_all("md-card", class_="comment")

        for cc in comment_cards:
            data['comments'].append({
                "author": cc.find("span", class_="md-title").text.replace("\n", ""),
                "text": cc.find("p", class_="content").text.strip(),
                "link": "https://www.tatoeba.org%s" % (cc.find("md-button", class_="md-icon-button").attrs['href']),
            })

        return HttpResponse(
            json.dumps(data),
            content_type='application/json',
        )

    except Exception as e:
        print(e)
        return HttpResponse(status=500)


@api_view(['GET'])
def languages(request):
    user_language = request.GET.get("user_language", "eng")

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
