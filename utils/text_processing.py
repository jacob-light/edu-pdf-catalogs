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


def get_char_list():
    return


def get_text_from_position(
    data, page_id, index_from, index_to=None, how_long=None, chars=False
):
    for page in data:
        if page["page"] == page_id:
            if index_to:
                till = index_to
            if how_long:
                till = how_long + index_from
            if chars:
                print(page["characters"]["size"][index_from:till])
            return "".join(page["characters"]["chars"])[index_from:till]
