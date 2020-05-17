def get_sentence_from_source(source):
    # The next two lines are absolutely the most horrible lines I've written in five years!

    direct = [{**t, "direct": True} for t in [{k: sentence[k] for k in ('text', 'id', 'lang')} for sentence in source[1]]]
    indirect = [{**t, "direct": False} for t in [{k: sentence[k] for k in ('text', 'id', 'lang')} for sentence in source[2]]]
    
    return {
        "translations": direct + indirect,
        "text": source[0]['text'],
        "lang": source[0]['lang'],
        "id": source[0]['id'],
    }


def build_search_url_from_request_data(request_data):

    searchText = request_data.get("text")

    if searchText is None:
        return None

    params = {
        "from": request_data.get("from", "und"),
        "to": request_data.get("to", "und"),
        "page": request_data.get("page", "1"),
        "user": request_data.get("user", ""),
        "orphans": request_data.get("orphans", "no"),
        "unapproved": request_data.get("unapproved", "no"),
        "has_audio": request_data.get("has_audio", ""),
        "tags": request_data.get("tags", ""),
        "list": request_data.get("list", ""),
        "native": request_data.get("native", ""),
        "trans_filter": request_data.get("limit", ""),
        "trans_to": request_data.get("trans_to", "und"),
        "trans_link": request_data.get("trans_link", ""),
        "trans_user": request_data.get("trans_user", ""),
        "trans_orphan": request_data.get("trans_orphan", ""),
        "trans_unapproved": request_data.get("trans_unapproved", ""),
        "trans_has_audio": request_data.get("trans_has_audio", ""),
        "sort": request_data.get("sort", "relevance"),
        "sort_reverse": request_data.get("sort_reverse", ""),
    }

    fragments = ["&{}={}".format(k, params[k]) for k in params]

    url = "https://www.tatoeba.org/eng/sentences/search?query=" + searchText

    for f in fragments:
        url += f

    return url
