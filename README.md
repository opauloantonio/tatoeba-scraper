# tatoeba-scraper
A small project that scraps Tatoeba search results and returns them as JSON.


## How to use it

The project is hosted on [Heroku](https://heroku.com) under https://tatoeba-scraper.herokuapp.com/

You can make requests to that server or run the project on your own machine. For that, just clone the repo and install the requirements:

- `python -m venv env`
- `source env/bin/activate` or if you're on Windows `.\env\Scripts\activate`
- `pip install -r requirements.txt`

Now, run the server with `python manage.py runserver`, you can safely ignore the warning about migrations since this project doesn't use a database. Or if you want to get rid of it, run `python manage.py migrate`

I recommend using the awesome library [HTTPie](https://github.com/jakubroztocil/httpie) for making requests directly from the command line, after running the server, you can make requests this way `http :8000/search/ text="hello"`


## Endpoints

There are four endpoints:

- /search/
- /sentence/\<int:id\>/
- /languages/
- /random/

### Search

This endpoint accepts a POST request with a `url` parameter. That URL should be the full URL for a search on Tatoeba.

If you don't provide a `url` parameter, you can provide many different parameters with the only mandatory one being `text`, here's a list of all possibilities:

- text
- from
- to
- user
- orphans
- unapproved
- has_audio
- tags
- list
- native
- trans_filter
- trans_to
- trans_link
- trans_user
- trans_orphan
- trans_unapproved
- trans_has_audio
- sort
- sort_reverse

If successful, it'll return an object with the fields **numberOfResults** which is a string and an array of objects called **sentences**. In sentences, each object represents a sentence with an **id**, **text** and **language** fields. Each of these objects have also a **translations** field, which is another array of objects, containing the translations for the sentence. Each object in the translations field also has a **direct** field, which is a boolean that indicates whether the sentence is a direct translation of the parent sentence or if it is a translation of a translation.

### Sentence

For this endpoint, you should provide an id for a sentence on Tatoeba, for instance: /sentence/277046/

If successful, it'll return an object with the fields **id**, **text** and **language** and an array with the translations of the sentence.

### Languages

Use this endpoint to get the list of all available languages on Tatoeba. It'll return an array of objects. Each object has the fields:

- **language**, which is the name for the language
- **code**, which is a unique three-letter code for each language as they appear in [ISO 639-2](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
- **img**, which is a URL for the svg icon for the language

You can also provide a GET parameter `lang` with one of the three-letter codes if you want get the names of the languages translated to a given language. The default is English.

### Random Sentence

Use this endpoint to get a random sentence. You can also provide a `lang` parameter to get a random sentence for a given language. The default is `und`, meaning that the language will also be random.

## Why did I build this?

Tatoeba doesn't provide an API and I had few project ideas that could really use one:

- an Android app with React Native
- a Chrome extension for faster searching 
- a web app for learning kanji which I'm working on right now, [you should take a look at it!](https://www.ryouflashcards.com)

Anyone is welcome to give feedback and help this project, if you use it in any project, I'd love to know!

## A warning

Tatoeba undergoes a lot of change. It's possible that the code in this project stops working at any given moment. I'll try to keep it up to date with the website's structure but there are no guarantees!
