#!/usr/bin/env python3
from collections import defaultdict
from itertools import chain
import math
import os
import re
import sys
import traceback
from typing import Dict, List, Tuple


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


def regex_pattern_ignore_whitespace(s):
    return r'\s*'.join(s.split())
    

def find(phrase, text, backward=10, forward=1000):
    """
    HELPER func, useless in process
    
    finds phrase in text, and returns surrounding
    characters (number of characters ranging from
    backward to forward)
    """
    idx = text.index(phrase)
    return text[idx - backward : idx + forward]


def find_department_font(page, department_name, avoid=None) -> Tuple[List,List]:
    """
    something to consider: works only on pages where header is 
    either equals to department from previous page, or department 
    starts on that page therefore the header equals to it, 
    or there is no header 
    
    - so logically that's how things should be printed
    
    the strategy against first rule not being followed by catalog,
    would be to have "avoid word"
    
    - mostly fixed, can't think of an edge case but life will probably 
    continue to suprise me
    """
    try:
        page_text = ''.join(page['characters']['chars'])
        offset = 0
        if avoid:
    #         print(regex_pattern_ignore_whitespace(avoid))
            avoid_matched = re.search(pattern=regex_pattern_ignore_whitespace(avoid),
                  string=page_text)
            offset = avoid_matched.end()
        f = re.search(pattern=regex_pattern_ignore_whitespace(department_name),
                  string=page_text[offset:])
        dep_font_size = page['characters']['size'][offset+f.start():offset+f.end()]
        dep_font_family = page['characters']['fontfamily'][offset+f.start():offset+f.end()]
    except:
        exception_text = f"""ERROR: can't find font details: (avoid={avoid}) {department_name} -> {regex_pattern_ignore_whitespace(department_name)}
{list(zip(page['characters']['chars'],page['characters']['size'],page['characters']['fontfamily']))}"""
        exception_text = exception_text[:50000-46001]
        print(len(exception_text))
        raise Exception(exception_text) # google cell can only hold 50000 characters
    try:
        txt_font_size = page['characters']['size'][offset+f.end()+10:offset+f.end()+20]
    except:
        txt_font_size = []
    
    return dep_font_size, dep_font_family, txt_font_size


    
def get_all_departments(data, department_font_sizes, department_font_family, margin_of_error=0.1):
    department_font_family.append(-1)
    deps = []
    for page in data:
        r = ''
        
        if len(page['characters']['chars']) != len(page['characters']['size']):
            raise Exception('rip')
        
        for i,(c,s,f) in enumerate(zip(page['characters']['chars'], 
                                   page['characters']['size'], 
                                   page['characters']['fontfamily'])):
            if (
                (
                 math.isclose(max(department_font_sizes), s, abs_tol=margin_of_error) 
                 or math.isclose(min(department_font_sizes), s, abs_tol=margin_of_error) 
                 or int(s) == -1
                ) 
                and f in department_font_family
               ):
                if c != '\n':
                    r += c
                    
            else:
                if r not in ['','\n'] and len(r) > 0:
                    if (r[0].isupper() 
                        and not has_numbers(r)):
                        deps.append((r,page['page']))
                        r = ''
    return deps
                
    
def departments_update_with_page_ranges(departments):
    result = []
    for idx,(dep,page) in enumerate(departments):
        if idx+1 != len(departments):
            next_department = departments[idx+1]
            next_department_name = next_department[0]
            next_department_page = next_department[1]
            result.append((dep, list(range(page,next_department_page+1))))

    return result
    

def merge_duplicate_departments(departments):
    deps = defaultdict(list)
    
    for d,pages in departments:
        if d in deps:
            deps[d] += pages
        else:
            deps[d] = pages
            
    return [(d,pages) for d,pages in deps.items()] 


def clear_junk_departments(departments):
    return [
        d for d in departments 
        if 'APPENDIX' not in d[0] # UCLA
    ]
    
def get_department_text_slice(data, departments, search_next_dep_reversed=True):
    for idx,(department_name, pages) in enumerate(departments):
        text_from_pages = ''
        for page in data:
            if page['page'] in pages:
                for text_box in page['tboxes']:
                    text_from_pages += text_box
            elif page['page'] > max(pages):
                break
        department_in_text = re.search(
            pattern=regex_pattern_ignore_whitespace(department_name),
            string=text_from_pages)
        try:
            department_text_index_start = department_in_text.start()
        except AttributeError:
            yield (department_name, f'''ERROR: match not found when searching for department 
            - {regex_pattern_ignore_whitespace(department_name)}''')
        department_text_index_end = None
        if len(departments) != idx + 1:
            next_department_name, next_department_pages = departments[idx+1]
        else:
            yield (department_name, text_from_pages[department_text_index_start:])
        
        if len(next_department_pages) == 0: 
            yield (department_name, Exception(f"next_department_pages is empty for next_department_name={next_department_name}"))
        if len(pages) == 0: 
            yield (department_name, Exception(f"department_pages is empty for department_name={department_name}"))
        
        if min(next_department_pages) == max(pages):
            if search_next_dep_reversed:
                ndn = next_department_name[::-1]
                tfp = text_from_pages[::-1]
                next_dep_index = lambda offset: (len(tfp)
                                                 - offset 
                                                 + len(ndn) 
                                                 - 1)
            else:
                ndn = next_department_name
                tfp = text_from_pages
                next_dep_index = lambda offset: offset - 1  
                
            try:
                next_department_in_text = re.search(
                    pattern=regex_pattern_ignore_whitespace(ndn),
                    string=tfp)
            except re.error:
                yield (department_name, f'''ERROR REGEX: match not found when searching for next department ({'reversed' if search_next_dep_reversed else 'not reversed'})
- {regex_pattern_ignore_whitespace(ndn)}\n{tfp}''')
                
            try:
                department_text_index_end = next_dep_index(next_department_in_text.start())
            except AttributeError:
                yield (department_name, f'''ERROR: match not found when searching for next department 
- {regex_pattern_ignore_whitespace(next_department_name[::-1])}''')
                
        yield (department_name, text_from_pages[department_text_index_start:department_text_index_end])
    
    
def get_courses(text, regex_pattern):

    regexed_courses = re.findall(
        pattern=regex_pattern,
        string=text, 
        flags=re.DOTALL
    )

    for course in regexed_courses:
        yield course
      
    