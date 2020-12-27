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
    """ returns True if there are any digits in string """
    return any(char.isdigit() for char in inputString)


def regex_pattern_ignore_whitespace(s):
    """ 
    converts 'hello world' to 'hello\s*world' 
    therefore allowing to match both `hello world` and 
    `hello
    world`
    """
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


def find_department_font(page: Dict, department_name: str, avoid=None) -> Tuple[List,List,List]:
    """
    # INPUT
    page = {
            'page':3,                                          <- page number
            'characters': {
              'size':      [11.0, 11.0, 11.0, 3.0, 3.0, ...],  <- size of each character from page, ordered from top to bottom
              'chars':     [ 'H',   'e',  'l','l',  'o', ... ] <- all characters from the page, ordered from top to bottom
              'fontfamily':[   0,     0,    0,  0,    2, ... ] <- font family for each character from the page, ordered from top to bottom
            },
            'tboxes': ['Hello\n', 'beautiful world']           <- grouping of characters called text boxes, ordered from top to bottom    
           }
    department_name = 'Biology'                                <- search phrase, when found, underlying font data is extracted 
    avoid = 'Biology 23'                                       <- search avoid phrase, when found text is sliced from that index to avoid matching underlying font data from avoid phrase
    

    # OUTPUT
    department_font_sizes = [18.0, 18.0, 18.0,...]             <- font size used for department name
    department_font_family = [1, 1, 1, ...]                    <- font family used for department name
    txt_font_size = [11.0, 11.0, 11.0, ...]                    <- font size for text after deparmtent name (DEADCODE: not used anywhere in the script)
 

    # NOTES
    works only on pages where 
    - header is either equals to department from previous page, 
    - or department starts on that page therefore the header equals to it, 
    - or there is no header 
    
    So logically that's how catalog should be printed.
    
    The strategy against first rule not being followed by catalog,
    would be to have "avoid word".
    
    Mostly stable, can't think of an edge case but life will probably 
    continue to suprise me.
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


    
def get_all_departments(data: List[Dict], department_font_sizes: List[float], 
                        department_font_family: List[int], margin_of_error=0.1) -> List[Tuple[str,int]]:
    """
    # INPUT
    data = list of pages, where page:
    page = {
            'page':3,                                          <- page number
            'characters': {
              'size':      [11.0, 11.0, 11.0, 3.0, 3.0, ...],  <- size of each character from page, ordered from top to bottom
              'chars':     [ 'H',   'e',  'l','l',  'o', ... ] <- all characters from the page, ordered from top to bottom
              'fontfamily':[   0,     0,    0,  0,    2, ... ] <- font family for each character from the page, ordered from top to bottom
            },
            'tboxes': ['Hello\n', 'beautiful world']           <- grouping of characters called text boxes, ordered from top to bottom    
           }
    department_font_sizes = [18.0, 18.0, 18.0,...]             <- font size used for department name
    department_font_family = [1, 1, 1, ...]                    <- font family used for department name


    # OUTPUT
    deps = [
        ('Biology', 123),   <- department name, deparment first page
        ('Chemistry', 234),
        ...
    ]
    """
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
    """
    # INPUT
    departmets = [
        ('Biology', 123),   <- department name, deparment first page
        ('Chemistry', 125),
        ('Computer Science', 127),
        ...
    ]


    # OUTPUT
    result = [
        ('Biology', [123,124,125]), 
        ('Chemistry', [125,126,127]),
        ('Computer Science', [127,...]),
        ...
    ]
    """
    result = []
    for idx,(dep,page) in enumerate(departments):
        if idx+1 != len(departments):
            next_department = departments[idx+1]
            next_department_name = next_department[0]
            next_department_page = next_department[1]
            result.append((dep, list(range(page,next_department_page+1))))

    return result
    

def merge_duplicate_departments(departments):
    """
    # INPUT
    departments = [
        ('Biology', [123,124]), 
        ('Biology', [125]), 
        ('Chemistry', [125,126,127]),
        ('Chemistry', [125,126,127]),
        ...
    ]


    # OUTPUT
    [
        ('Biology', [123,124,125]), 
        ('Chemistry', [125,126,127]),
        ...
    ]
    """
    deps = defaultdict(list)
    
    for d,pages in departments:
        if d in deps:
            deps[d] += pages
        else:
            deps[d] = pages
            
    return [(d,pages) for d,pages in deps.items()] 


def clear_junk_departments(departments):
    """
    # INPUT
    departments = [
        ('Biology', [123,124,125]), 
        ('Chemistry', [125,126,127]),
        ('APPENDIX', [234,235,236,237])
    ]


    # OUTPUT
    [
        ('Biology', [123,124,125]), 
        ('Chemistry', [125,126,127]),
    ]
    """
    return [
        d for d in departments 
        if 'APPENDIX' not in d[0] # UCLA
    ]
    

def get_department_text_slice(data, departments, search_next_dep_reversed=True):
    """
    # INPUT
    data = list of pages, where page:
    page = {
            'page':3,                                          <- page number
            'characters': {
              'size':      [11.0, 11.0, 11.0, 3.0, 3.0, ...],  <- size of each character from page, ordered from top to bottom
              'chars':     [ 'H',   'e',  'l','l',  'o', ... ] <- all characters from the page, ordered from top to bottom
              'fontfamily':[   0,     0,    0,  0,    2, ... ] <- font family for each character from the page, ordered from top to bottom
            },
            'tboxes': ['Hello\n', 'beautiful world']           <- grouping of characters called text boxes, ordered from top to bottom    
           }
    departments = [
        ('Biology', [123,124,125]), 
        ('Chemistry', [125,126,127]),
        ('APPENDIX', [234,235,236,237])
    ]
    search_next_dep_reversed=True                              <- when building text slice from current department to next department, 
                                                                  look for next department starting from the bottom of the page

    # OUTPUT, iteratively (one by one)
    ('Biology', "Biology\n Courses:\n123B. Biology basics\n234B. Bio advanced......")
    """
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
    """
    # INPUT
    text = "Biology\n Courses:\n123B. Biology basics\n234B. Bio advanced......
    regex_pattern - pattern to capture courses

    # OUTPUT, iteratively (one by one)
    '123B. Biology'     
    (next iteration)
    '234B. Bio advanced'
    """
    regexed_courses = re.findall(
        pattern=regex_pattern,
        string=text, 
        flags=re.DOTALL
    )

    for course in regexed_courses:
        yield course
      
    
