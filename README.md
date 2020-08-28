# bytes-into-baking
<img align="right" src="img/croissant-display.JPG" width='500' height='auto' ></img>

## Overview
- Food is one of the most common topics on the internet, with content being published on the web by big businesses such as *foodnetwork* and *allrecipes* to home chefs writing their own blogs. 
- Food is trendy--keeping on top of food trends could be valuable to people who write about food and publish recipes.
### A utility pastry recipe web scraper
- Can one write a utility web scraper to grab recipes from websites that is general enough to work across a variety of website and copy structures?
### Turning the recipe documents into vectors for a supervised machine learning classifier problem
- How well do the recipe instructions predict the type of recipe?
- If the predictive power is good, what are the key words that the model is relying upon?
- Can an unsupervised model look within a particular recipe class to identify different schools of thought for that particular product? E.g. Can it identify different types of croissant recipes?
### Looking towards the future
- Can a model that scrapes the web to keep the pulse on the food world detect differences in regional food culture? Can a model identify changes in food trends before they are generally recognized by the public? Can a model uncover interesting, yet poorly recognized food histories?
### Goals
- Generate a list of target websites for a particular recipe class by pulling urls from Google search
- Develop a utility scraper to identify recipes and then grab pertinent information about the recipe from the recipe section--starting with instructions
- Test the results of the scraper on a supervised model that classifies the vectorized recipes
- Explore the possibiliity of identifying different groupings within a specific recipe class

## Tools and techniques used in this project
- **Tools**
> - Python, Beautiful Soup, Pandas, Numpy, Gensim
- **Visualization**
> - Matplotlib, Plotly
- **Techniques**
> - Web-scraping, Multinomial Naive Bayes Classification, Non-negative Matrix Factoring (NMF)

## Preliminary EDA
### Searching for croissant baking temperatures
- Searches for 'croissant bake temperature' or 'temperature cuisson croissant' were conducted on Google country-specific search sites for the US, UK, and France. The first 100 links were obtained for each country. These links were subsequently scraped to determine if they were a croissant baking recipe, and if so, for their initial baking temperature.
- Baking temperatures were found by looking for sentences that contained the words 'preheat', 'bake', or 'oven' followed by a 3 digit number followed by a temperature indicator. 
- Croissant baking often employs a two-stage approach with a high starting temp followed by a lower finishing temp. The script pulled the first temperature mention, so this is the starting temp.
- For the US graphic, websites were excluded if the first temperature mention was in celsius.
- For the UK and French graphics, websites were excluded if the first temperature mention was in fahrenheit.
### Results from the Preliminary EDA phase
- Of the 140 links obtained from the Google search by country, 50+ usable temperatures were obtained for the US distribution and for the French distribution.
- Only 12 usable temperatures were obtained for the UK distribution. This is likely due to many recipes of US origin appearing in the google.uk search and being filtered out due to our restriction that temps needed to be expressed primarily in celsius.
- Mean temperatures are higher in the US than in France or the UK. Means testing has not been performed yet.
- The distributions are slightly different for the countries with France having what appears to be a slightly right-skewed distribution compared to the US distribution.
<img align="left" src="img/us-croissant-baketemp-distribution.png" width='500' height='auto' ></img>
<pre>











</pre>
<img align="left" src="img/fr-croissant-baketemp-distribution.png" width='500' height='auto' ></img>
<pre>










</pre>
<img align="left" src="img/uk-croissant-baketemp-distribution.png" width='500' height='auto' ></img>
<pre>


















</pre>
## Web scraper design

### A focus on pastry recipes
- I chose to start with pastry recipes since I come with an indepth knowledge of this space. I've explored hundreds of pastry recipe websites over my career.
- I chose four categories of pastry and baked goods recipes that had what I considered to be important differences, yet enough similarity that they might confuse a model.

### Numerous ways to format a recipe, but some intriguing similarities make a utility scraper possible
- My initial Google search website 'spider' yielded more than recipe websites--I needed a scraper that would limit the possibility of seeing a recipe when one wasn't there
- More than a third of recipes I encountered follow a schema format promoted by Yoast, a website schema publisher to aid in SEO optimization--useful tags and a json structure with standardized keys for things like recipe ingredients and instructions (Yeah!)
- Another 40-50% placed the body of their recipe in a script tag with one of several commonly used attributes. This wasn't as clean of an approach--I usually ended up with extra text--but I still was able to get some results
- The rest, well, some didn't want to be scraped, and some had unusual structures. I could spend a lot of time chasing the tail with limited utility.

### Results

- First pass links from Google search | Usable recipes obtained |  Yield
- Brioche               | 112       | 55     | 49%
- Ciambellone           | 116       | 55     |  47%
- Croissant             | 180       | 72     | 40%
- Puff pastry           | 200       | 86     | 43%




## Future Directions
- Develop a spider to crawl targeted websites instead of relying on Google search
- Improve the search web-scraping function to obtain a better yield
- Replace search with an unsupervised NLP model
- Explore other parameters of croissant preparation and baking.
- Explore the comments for the various websites to determine if people in the respective countries interact differently with recipe authors.
- Once the tools are in good shape, use them to explore other food topics.
