import collections.abc as clct
import json
import re
import time

import bs4
import lxml
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from lxml import html
from selenium import webdriver


class Recipe(dict):
    """Recipe object that stores information of a recipe in a dictionary like object"""

    def __init__(
        self,
        page_family: str = "",
        page_species: str = "",
        url: str = "",
        language: str = "",
        recipe_name: str = "",
        cook_time: str = "",
        ingredients: str = "",
        instructions: str = "",
    ):

        self.page_family = page_family
        self.page_species = page_species
        self.url = url
        self.language = language
        self.recipe_name = recipe_name
        self.cook_time = cook_time
        self.ingredients = ingredients
        self.instructions = instructions

    def __repr__(self):
        return repr(self.__dict__)

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]


class ScrapePage:
    """Webpage scraping object"""

    def __init__(self, page_family, page_species, search_pattern_1, search_pattern_2):
        self.search_pattern_1 = search_pattern_1
        self.search_pattern_2 = search_pattern_2
        self.page_family = page_family
        self.page_species = page_species

    def scrape_page(self, url) -> Recipe:

        res = {
            "page_family": "",
            "page_species": "",
            "url": url,
            "language": "",
            "recipe_name": "",
            "cook_time": "",
            "ingredients": "",
            "instructions": "",
        }

        header_map = [{"User-Agent": "Mozilla/5.0"}, {"User-Agent": "XY"}, {}]

        target_xpath = "//html/@lang"

        try:
            for header in header_map:
                r = requests.get(url, allow_redirects=False, headers=header)
                time.sleep(0.5)
                if r.status_code == 200:
                    print(f"Success {r.status_code}, {url}")
                    break
                    
            if r.status_code != 200:
                print(f"Fail {r.status_code}, {url}")
                return Recipe(**res)

            root = lxml.html.fromstring(r.text)
            language_construct = root.xpath(target_xpath)

            if language_construct:
                language = language_construct[0].split("-")[0]

            soup = BeautifulSoup(r.content, "html")
            json_data = soup.findAll(type="application/ld+json")
            
            page_genus = ''
            page_family = ''
            page_species = ''
            language = ''
            recipe_name = ''
            cook_time = ''
            ingredients = ''
            instructions = ''


            # For sites that follow schema.org for 'Recipe'
            if len(json_data) > 0:                
                    for i in range(len(json_data)):
                        data = json.loads(json_data[i].string)
                        check = self.find_value_of_nested_dict_or_list(data,'recipeInstructions')
                        
                        instr = []
                        
                        if check:
                            if isinstance(check[0], dict) and instr == []:
                                instr = [x.get('text', '') for x in check]     
                                instructions = ''.join(instr)
                            else:
                                instructions = ''.join(check)
                        
                        ingredients = self.find_value_of_nested_dict_or_list(data,'recipeIngredient')
                        recipe_name = self.find_value_of_nested_dict_or_list(data,'name')
                        cook_time = self.find_value_of_nested_dict_or_list(data,'cookTime')

                # For sites that do not follow schema.org for 'Recipe'
            if len(json_data) == 0 or self.find_value_of_nested_dict_or_list(data,'recipeInstructions') == False:     
                    result = soup.find_all('div', attrs={'class': ['body entry-content', 'entry-content', 
                                                                   'hrecipe', 'post-entry', 'post-content', 
                                                                   'post-content__body','recept', 'recipe-content']})
                    soup_string = ''
                    for r in result:
                        soup_string += str(r.text)
                    instructions = soup_string
              
            res = {
            "page_genus": "",
            "page_family": "",
            "page_species": "",
            "url": url,
            "language": language,
            "recipe_name": recipe_name,
            "cook_time": cook_time,
            "ingredients": ingredients,
            "instructions": instructions,
        }
            return Recipe(**res)

        except Exception as e:
            print("Exception", e)
            return Recipe(**res)
        

    def find_value_of_nested_dict_or_list(self, a, our_key):
        if not isinstance(a, clct.Iterable):
            return False
        if isinstance(a, str):
            return False
        if isinstance(a, list):
            for item in a:
                result = self.find_value_of_nested_dict_or_list(item, our_key)
                if result:
                    return result
        if isinstance(a, dict):
            for key in a:
                if key == our_key:
                    return a[our_key]
                else:
                    result = self.find_value_of_nested_dict_or_list(a[key], our_key)
                    if result:
                        return result
        return False
