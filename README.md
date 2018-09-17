# tatoeba-scraper
A small project that scraps Tatoeba search results and returns them as JSON.


## How to use it

The project is hosted on [Heroku](https://heroku.com) under https://tatoeba-scraper.herokuapp.com

It accepts a POST request with a `url` parameter. That URL should be the full URL for a search on Tatoeba, for instance: https://tatoeba.org/eng/sentences/search?query=Let%27s%20go&from=eng&to=und&sort=words

It'll return an array of objects, each object represents a sentence with an **id**, **text** and **language** fields. Each of these objects have also a **translations** field, which is another array of objects, containing the translations for the sentence. Each object in the translations field also has a **direct** field, which is a boolean that indicates whether the sentence is a direct translation of the parent sentence or if it is a translation of a translation.

## TODO

- [x] Include number of results in response.
- [ ] Create view to scrap the page with the details of a sentence. 

## Why did I build this?

As I'm trying to learn more about web and app development, I decided to create a mobile app for Tatoeba to learn more and practice my current skills. Unfortunately, Tatoeba doesn't provide an API as of now and it's built using PHP and CakePHP. I'm a Python programmer with focus on Django. I believe it would take much longer to learn PHP, join the dev team, create an API to the website than it would take to create this and use it in my native apps. That's why this project exists.
