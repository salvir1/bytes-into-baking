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
        page_genus: str = "",
        page_family: str = "",
        page_species: str = "",
        url: str = "",
        language: str = "",
        recipe_name: str = "",
        cook_time: str = "",
        ingredients: str = "",
        instructions: str = "",
    ):

        self.page_genus = page_genus
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




class ScrapeRecipe:
    
    default_headers = [{"User-Agent": "Mozilla/5.0"}, {"User-Agent": "XY"}, {}]
    
    def __init__(self,
                page_genus : str = "",
                page_family : str = "",
                page_species : str = "",
                re_pattern_1 : str = "",
                re_pattern_2 : str = ""):
        """Recipe object that stores information of a recipe in a dictionary like object"""

        self.page_genus = page_genus
        self.page_family = page_family
        self.page_species = page_species
        self.re_pattern_1 = re_pattern_1
        self.re_pattern_2 = re_pattern_2
        self.current_language = ''
        

    def process_url(self, url:str, headers:list=[], verbose:bool=False, idx:str='', extract_lang:bool=False) -> Recipe:
        content = self.cycle_header(url, headers=headers, verbose=verbose, idx=idx, extract_lang=extract_lang)
        json_content = self.load_json(content)
        
        parsed_data = self.parse_data(json_content)
        time.sleep(0.25)
        
        if extract_lang:
            parsed_data['language'] = self.current_language
        
        parsed_data['url'] = url
        parsed_data['page_genus'] = self.page_genus
        parsed_data['page_family'] = self.page_family
        parsed_data['page_species'] = self.page_species

        # Check if instructions exist
        if parsed_data.get('instructions', None) == None:
            instructions = self.alternate_instructions(url)
            parsed_data['instructions'] = instructions
        
        
        return Recipe(**parsed_data)
        
        
    def cycle_header(self, url:str, headers:list=[], verbose:bool=False, idx:str='', extract_lang:bool=False) -> str:
        '''1: Returns target uncoded json string from URL for further parsing'''
        header_map = headers if headers else self.default_headers
        res = None

        for header in header_map:
            try:
                req = requests.get(url, allow_redirects=False, headers=header)
                if req.status_code == 200:
                    break
            except Exception as msg:
                print('Exception', msg)
                return res

        soup = BeautifulSoup(req.content, 'html')
        pool = [x.string for x in soup.findAll(type="application/ld+json") if x.string]
        
        # Extract Language
        if extract_lang:
            self.current_language = self.extract_language(req)
        
        # Extract main content
        if pool:
            res = max(pool, key=len)

        access_result = "Success" if req.status_code == 200 and res else "Failure"
        if verbose:
            print(f'{idx} {access_result} with code {req.status_code} at URL: {url}')

        return res
    
    def alternate_instructions(self, url:str='') -> str:
        res = ''
        call = requests.get(url)
        if call.status_code == 200:
            soup = BeautifulSoup(call.content)
            result = soup.find_all('div', attrs={'class': ['body entry-content', 'entry-content', 
                                                           'hrecipe', 'post-entry', 'post-content', 
                                                           'post-content__body','recept', 'recipe-content']})
            for r in result:
                res += str(r.text)
        return res

    
    def extract_nested_instructions(self, content:any, key_:str='') -> str:
        res = content.get(key_)
        if res != None and not isinstance(res, str):
            if isinstance(res, list):
                res = ' '.join([i.get('text', '') for i in res if isinstance(i, dict)])
        
        return res
    
    def extract_language(self, response:requests.models.Response) -> list:
        res = ''
        if response.text:
            target_xpath = "//html/@lang"
            root = lxml.html.fromstring(response.text)
            language_construct = root.xpath(target_xpath)

            if language_construct:
                res = language_construct[0].split("-")[0]

        return res
    

    def x_strip(self, string:str, seq:list=['\n', '\t']) -> str:
        """Strips all newline and tab escape instances from string"""
        return string.replace('\n', '').replace('\t', '')
    

    def load_json(self, string:str) -> dict:
        """2: Returns dictionary from tag string, if result of json.loads is not dict object, largest dict object will be used"""
        res = {}
        if string:
            stripped = self.x_strip(string)
            try:
                converted = json.loads(stripped)
                res = converted
            except:
                pass

        if isinstance(res, list):
            res = max(res, key=len)
        return res
    

    def get_root(self, raw:dict) -> dict:
        '''Given a json decoded dictionary, returns target root dictionary object'''
        res = {}
        if raw:
            trg_key = next(x for x in raw if not isinstance(raw[x], str))
            nest = raw[trg_key]

            for dict_ in nest:
                find = dict_.get('@type')
                if isinstance(find, str) and find.lower().strip() == 'recipe':
                    res = dict_
                    break

        return res


    def parse_data(self, raw:dict) -> dict:
        '''3: Parses needed information from raw json parsed dictionary object'''
        res = {}
        if raw:
            # Pre-processing
            if len(raw.keys()) <= 2:
                raw = self.get_root(raw)
                
            res['instructions'] = self.extract_nested_instructions(raw, 'recipeInstructions')
            
            
            res['ingredients'] = self.extract_nested_instructions(raw, "recipeIngredient")
            res['recipe_name'] = self.extract_nested_instructions(raw, "name")
            res['cook_time'] = self.extract_nested_instructions(raw, "cookTime")
            
            
            
#         res = raw
        return res





