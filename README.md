# tatoeba-scraper
A small project that scraps Tatoeba search results and returns them as JSON.


## How to use it

The project is hosted on [Heroku](https://heroku.com) under https://tatoeba-scraper.herokuapp.com/

There are two endpoints:

- /search/
- /sentence_details/

### Search

This endpoint accepts a POST request with a `url` parameter. That URL should be the full URL for a search on Tatoeba, for instance: https://tatoeba.org/eng/sentences/search?query=Let%27s%20go&from=eng&to=und&sort=words

It's up to the user to supply the correct scheme of URL parameters to narrow the search effectively.

If successful, tt'll return an array of objects, each object represents a sentence with an **id**, **text** and **language** fields. Each of these objects have also a **translations** field, which is another array of objects, containing the translations for the sentence. Each object in the translations field also has a **direct** field, which is a boolean that indicates whether the sentence is a direct translation of the parent sentence or if it is a translation of a translation.

### Sentence Details

This endpoint accepts a POST request with a `url` parameter. That URL should be the full URL for the page with the details of a sentence on Tatoeba, for instance: https://tatoeba.org/eng/sentences/show/105511

If successful, it'll return an array with the translations of the sentence.

## TODO

- [x] Include number of results in response.
- [x] Create view to scrap the page with the details of a sentence. 

## Why did I build this?

Tatoeba doesn't provide an API and I have a few project ideas that could really use one:

- an Android app with React Native
- a Chrome extension for faster searching 
- a web app for learning kanji which I'm working on right now, [you should take a look at it!](https://www.ryouflashcards.com)

Anyone is welcome to give feedback and help this project, if you use it in any project, I'd love to know!