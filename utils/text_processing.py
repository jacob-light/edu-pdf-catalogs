#!/usr/bin/env python3


def find(phrase, text, backward=10, forward=1000):
    """
    finds phrase in text, and returns surrounding
    characters (number of characters ranging from
    backward to forward)
    """
    idx = text.index(phrase)
    return text[idx - backward : idx + forward]


def get_departments(path, pages=27, department_font_size=17):
    """ TODO """
    department_courses = defaultdict(str)
    department_name = ""
    past_department_name = False

    if c.size > department_font_size:
        if past_department_name:
            department_name = ""
        department_name += c.get_text()
        past_department_name = False
    else:
        past_department_name = True
    department_courses[department_name] += obj.get_text()

    return department_courses
