# tatoeba-scraper
A small project that scraps Tatoeba search results and returns them as JSON.


## How to use it

The project is hosted on [Heroku](https://heroku.com) under https://tatoeba-scraper.herokuapp.com/

There are three endpoints:

- /search/
- /sentence_details/
- /languages/

### Search

This endpoint accepts a POST request with a `url` parameter. That URL should be the full URL for a search on Tatoeba, for instance: https://tatoeba.org/eng/sentences/search?query=Let%27s%20go&from=eng&to=und&sort=words

It's up to the user to supply the correct scheme of URL parameters to narrow the search effectively.

If successful, it'll return an object with the fields **numberOfResults** which is a string and an array of objects called **sentences**. In sentences, each object represents a sentence with an **id**, **text** and **language** fields. Each of these objects have also a **translations** field, which is another array of objects, containing the translations for the sentence. Each object in the translations field also has a **direct** field, which is a boolean that indicates whether the sentence is a direct translation of the parent sentence or if it is a translation of a translation.

### Sentence Details

This endpoint accepts a POST request with a `url` parameter. That URL should be the full URL for the page with the details of a sentence on Tatoeba, for instance: https://tatoeba.org/eng/sentences/show/277046

If successful, it'll return an object with the fields **id**, **text** and **language** and an array with the translations of the sentence.

### Languages

Use this endpoint to get the list of all available languages on Tatoeba. It'll return an array of objects. Each object has the fields:

- **language**, which is the name for the language
- **code**, which is a unique three-letter code for each language as they appear in [ISO 639-2](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
- **img**, which is a URL for the svg icon for the language

## Why did I build this?

Tatoeba doesn't provide an API and I had few project ideas that could really use one:

- an Android app with React Native
- a Chrome extension for faster searching 
- a web app for learning kanji which I'm working on right now, [you should take a look at it!](https://www.ryouflashcards.com)

Anyone is welcome to give feedback and help this project, if you use it in any project, I'd love to know!

## A warning

Tatoeba undergoes a lot of change. It's possible that the code in this project stops working at any given moment. I'll try to keep it up to date with the website's structure but there are no guarantees!
