# bytes-into-baking

## Overview
- Food is trendy, in that what we put on our tables is constantly and dramatically being reshaped by the latest food trends. New food trends seemingly appear overnight and disappear just as quickly. 

- Can a model that scrapes the web to keep the pulse on the food world detect differences in regional food culture? Can a model identify changes in food trends before they are generally recognized by the public? Can a model uncover interesting, yet poorly recognized food histories?

## Goals
- The first phase of this project--a small step--was to determine if croissant baking instructions vary between the US, UK, and France. 
This is an ongoing project. New information will be added soon.

## Tools and techniques used in this project
- **Tools**
> - Python, Jupyter Lab, Beautiful Soup, Pandas, Numpy
- **Visualization**
> - Matplotlib
- **Techniques**
> - Web-scraping

## Data and EDA

### Searching for croissant baking temperatures
- Searches for 'croissant bake temperature' or 'temperature cuisson croissant' were conducted on Google country-specific search sites for the US, UK, and France. The first 100 links were obtained for each country. These links were subsequently scraped to determine if they were a croissant baking recipe, and if so, for their initial baking temperature.
- Baking temperatures were found by looking for sentences that contained the words 'preheat', 'bake', or 'oven' followed by a 3 digit number followed by a temperature indicator. 
- Croissant baking often employs a two-stage approach with a high starting temp followed by a lower finishing temp. The script pulled the first temperature mention, so this is the starting temp.
- For the US graphic, websites were excluded if the first temperature mention was in celsius.
- For the UK and French graphics, websites were excluded if the first temperature mention was in fahrenheit.


## Results

- Of the 100 links obtained from the Google search by country, 35-40 usable temperatures were obtained for the US distribution and for the French distribution.
- Only 10 usable temperatures were obtained for the UK distribution. This is likely due to many recipes of US origin appearing in the google.uk search and being filtered out due to the restriction that temps needed to be expressed primarily in celsius.
- Mean temperatures are similar for all three countries.
- The distributions are different for the countries with the US having a narrower distribution of initial baking temperature and the French distribution being wider.

- <img align="left" src="img/us-croissant-baketemp-distribution.png" width='500' height='auto' ></img>
<pre>











</pre>
- <img align="left" src="img/fr-croissant-baketemp-distribution.png" width='500' height='auto' ></img>
<pre>










</pre>
- <img align="left" src="img/uk-croissant-baketemp-distribution.png" width='500' height='auto' ></img>
<pre>

















</pre>
## Future Directions
- Seek to obtain more usable temperatures by grabbing more links from Google and/or by refining the sifting of the websites to obtain a better yield.
- Consider how best to compare the distributions.
- Explore other parameters of croissant preparation and baking.
- Explore the comments for the various websites to determine if people in the respective countries interact differently with recipe authors.
