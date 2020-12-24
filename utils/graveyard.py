# 🚪 YOU ARE ENTERING GRAVEYARD 💀


def save_oauth():
    from utils.dataframe import db2df, get_db_items
#     df_mapping = get_mapping()
#     df_mapping.to_csv('tempmapping.csv')
    df_mapping = pd.read_csv('tempmapping.csv')
    
break_count = lambda c: eval('break') if c==0 else c-1


def clear_junk_rows(df: pd.DataFrame, college: str, filename: str) -> pd.DataFrame:
    if college == 'UCLA':
        df = df[~df.department.str.contains("APPENDIX")]
        
    return df


def get_shifted_key(d:dict, k:str, offset:int) -> str:
    l = list(d.keys())
    if k in l:
        i = l.index(k) + offset
        if 0 <= i < len(l):
            return l[i]
    return None 




def iterhelper():
    counter = 10
    for d in departments.items():
        print(d)
        if counter == 0:
            break
        counter -= 1
    print(f'file:///home/marcin/Projects/upwork/Jacob/data/{college}/{filename}')
    if input('continue?') not in ['n','no']: 
        break
        
        
        
def course_sniper_regexs():
    ucla = (
    #     r"\n[A-Z]{0,2}[0-9]{2,4}[A-Z]{0,2}\.\ \ [.\.\s\w\n]*"
#     [\w\s\-\:\,\.\(\)\/.]*"
#     r"("
#     r"\n(?P<id>[A-Z]{0,2}[0-9]{2,4}[A-Z]{0,2})"                       # course ID
#     r"\.\ {1,2}"                                                      # spacing      
#     r"(?P<title>[A-Za-z:\s\n\.]*)"                                    # course title
#     r"\((?P<num>[0-9a-z\s\-]*)\)"                                       # magic number
#     r"(?P<decs>[.\n\s]*)"                                                            # course description
#     r")" #\.\ \(([0-9\ A-Z-a-z])\)"
# )
    )
    
    ohio = (
        r"("
            r"\n("                           # course ID
                r"([0-9]{4}\.[0-9A-Z]{3})"     # e.g. 2367.07S
                r"|([0-9]{4}\.[0-9]{2})"       # e.g. 2367.04
                r"|([0-9]{4}[H])"              # e.g. 4780H
                r"|([0-9]{4})"                 # e.g. 3080
            r")"
           r"\n([A-Za-z\s]*)"                # course title
           r"\nU\n"                          # letter U
           r"(.*?)"                          # course desrciption
           r"\n([0-9]{1,2})"                 # number to the right of letter U
         r")",
    )
    
    bowdoin = (
      r"("
                    r"\n\n([A-Z]{4}(\s|\\xa0)[0-9]{4})"  # course id
                    r"(.*?)\n"                           # course title
                    r"(.*?)"                             # course subtitle
                    r"\s([0-9]{1,3})\."                  # course enrolment limit
                    r"((?:(?![\n]{1}[A-Z]{4}).)*)"       # course description 
                                                          # UNTIL next course id 
                                                          # but not including it
                r")",
           r"("
                    r"\n\n([A-Z]{4}(\s|\\xa0)[0-9]{4})"  # course id
                    r"(.*?)\n"                           # course title
                    r"(.*?)"                             # course subtitle
                    r"\s([0-9]{1,3})\."                  # course enrolment limit
                    r"((?:(?![\n]{1}[A-Z]{4}).)*)"       # course description 
                                                          # UNTIL next course id 
                                                          # but not including it
                r")",
    )
    
    arkansas = (
    r"(\n\n?[A-Z]{3,4}\s[0-9]{3,4}.*)"
    )
    
def arkansas():
    df_arkansas = db2df(college='Arkansas')
    # df_arkansas.head()
    pd.concat(df_arkansas.pdfminer.map(lambda s: re.findall(r"(\n\n?[A-Z]{3,4}\s[0-9]{3,4}.*)", s)).map(pd.DataFrame).values[0:2])
    
def bowdoin():
    df_bowdoin = pd.concat(bowdoin_dfs)
    df_bowdoin['title'] = df_bowdoin['title'].str.replace('\n','')
    # df_bowdoin['title'] = df_bowdoin['title'].str.replace(r'\x','')
    df_bowdoin['desc'] = df_bowdoin['desc'].str.replace('\n','')
    # df_bowdoin['desc'] = df_bowdoin['desc'].str.replace(r'\x','')
    df_bowdoin = df_bowdoin.applymap(lambda x: x.encode('unicode_escape').
                     decode('utf-8') if isinstance(x, str) else x)
    with pd.ExcelWriter('data/bowdoin.xlsx') as writer: 
        df_bowdoin.to_excel(writer, sheet_name='data')
    df_bowdoin

    # find = "AFRS 1012"
    # bs[bs.index(find)-10:bs.index(find)+2000]
    bowdoin_dfs = []
    for file in tqdm(os.listdir('data/Bowdoin')):
        text = pdf_to_text(f"data/Bowdoin/{file}")
        if '202' in file:
            data = [{'id':r[1],'title':r[3],'sub':r[4],'desc':r[6],'num':r[5],'catalog':file} 
                for r in re.findall(
                    r"("
                        r"\n\n([A-Z]{4}(\s|\\xa0)[0-9]{4})"  # course id
                        r"(.*?)\n"                           # course title
                        r"(.*?)"                             # course subtitle
                        r"\s([0-9]{1,3})\."                  # course enrolment limit
                        r"((?:(?![\n]{1}[A-Z]{4}).)*)"       # course description 
                                                              # UNTIL next course id 
                                                              # but not including it
                    r")",
                    text,
                    re.DOTALL)
            ]
        else: #pre 2020
            data = [{'id':r[1],'title':r[3],'sub':None,'desc':r[4],'num':None,'catalog':file} 
                    for r in re.findall(
                    r"("
                        r"\n([0-9]{2,3}[a-z]{0,1})(\.\s|\s-)"  # course id
                        r"(.*?)\n"                           # course title
                        r"((?:(?!\n([0-9]{2,3}[a-z]{0,1})(\.\s|\s-)).)*)"  # UNTIL next course id but not including
                    r")",
                    text,
                    re.DOTALL)
            ]

        bowdoin_dfs.append(pd.DataFrame(data))

        df_bowdoin = pd.concat(bowdoin_dfs)
        df_bowdoin['title'] = df_bowdoin['title'].str.replace('\n','')
        # df_bowdoin['title'] = df_bowdoin['title'].str.replace(r'\x','')
        df_bowdoin['desc'] = df_bowdoin['desc'].str.replace('\n','')
        # df_bowdoin['desc'] = df_bowdoin['desc'].str.replace(r'\x','')
        df_bowdoin = df_bowdoin.applymap(lambda x: x.encode('unicode_escape').
                         decode('utf-8') if isinstance(x, str) else x)
        with pd.ExcelWriter('data/bowdoin.xlsx') as writer: 
            df_bowdoin.to_excel(writer, sheet_name='data')
        df_bowdoin
   

def ohio():
    df_ohiostate = db2df(college='Ohio State')
    df_ohiostate.head()
    ohio_sample = pypdf2txt("data/Ohio State/course_catalog_2010_2011.pdf")
    d=get_all_data("data/Ohio State/Ohio State_2014-2015.pdf", 4)
    ohio_dfs = []
    for file in tqdm(os.listdir('data/Ohio State')):
        # better to use pdf2txt, otherwise the number to the left of letter U
        # sometimes flotes away from the course it is assigned to
        ohs2 = pdf2txt(f"data/Ohio State/{file}")

        data = [{'id':r[1],'title':r[6],'desc':r[7],'num':r[8],'catalog':file} 
         for r 
         in re.findall(
             r"("
                r"\n("                           # course ID
                    r"([0-9]{4}\.[0-9A-Z]{3})"     # e.g. 2367.07S
                    r"|([0-9]{4}\.[0-9]{2})"       # e.g. 2367.04
                    r"|([0-9]{4}[H])"              # e.g. 4780H
                    r"|([0-9]{4})"                 # e.g. 3080
                r")"
               r"\n([A-Za-z\s]*)"                # course title
               r"\nU\n"                          # letter U
               r"(.*?)"                          # course desrciption
               r"\n([0-9]{1,2})"                 # number to the right of letter U
             r")",
             ohs2, 
             re.DOTALL) 
        ]
        ohio_dfs.append(pd.DataFrame(data))  

    df_ohio = pd.concat(ohio_dfs)
    df_ohio['title'] = df_ohio['title'].str.replace('\n','')
    df_ohio['desc'] = df_ohio['desc'].str.replace('\n','')
    with pd.ExcelWriter('data/ohio.xlsx') as writer: 
        df_ohio.to_excel(writer, sheet_name='data')
    df_ohio


    departments_mappings = []
    for file in tqdm(os.listdir('data/Ohio State')):
        mapping = get_departments(f"data/Ohio State/{file}")
        cleaned_mapping = dict()
        department_to_courses_ids_mapping = dict()

        for k,v in mapping.items():
            if len(v) > 50:
                cleaned_mapping[k] = v


        for k,v in cleaned_mapping.items():
            for r in re.findall(r'\n [0-9]{3,4}[\.0-9]{0,3}H?\n', v):
                department_to_courses_ids_mapping[r.strip()] = k

        try:
            departments_mappings.append(pd.Series(department_to_courses_ids_mapping, name=file))
        except:
            pass


def bad_way_to_do_this():
    """
    from itertools import chain
from IPython.display import clear_output

final = []
# df_mapping = get_mapping()
strip_whitespace = lambda s: s.replace('\n','').replace(' ','')
regex_until_but_not_including = lambda rgx: rf"(?:(?!{rgx}).)*"
regex_everything_not_greedy = '.*?'
regex_or = lambda iterable: '(' + '|'.join([f'({e})' for e in iterable]) + ')'
college = 'Ohio State'

for t in tqdm(df_mapping[(df_mapping.college == college) & ((df_mapping.scrape_me == 'TRUE') | (df_mapping.scrape_me))].itertuples()):
    clear_output()
#     print(t)
    while True:
        regex_course_pattern = (t.regex_pattern_course_id 
            + regex_everything_not_greedy 
            + regex_until_but_not_including(t.regex_pattern_course_id))
        filename = t.filename
    #     college = t.college
        df = db2df(college=college, filename=filename)
#         first_department_name = strip_whitespace(t.first_department_name)
        first_department_name = t.first_department_name
        avoid_matching_depatment_name = t.avoid_first_department_name if t.avoid_first_department_name else None 
        first_page = int(t.first_department_page)
        last_page = int(t.last_department_page)
        data = df[df.filename == filename].pdfminer_detailed.iat[0]    
        valid_data = data[first_page-1:last_page-1]

        department_font_sizes, department_font_family, paragraph_font_sizes = find_department_font(page=valid_data[0], 
                                                                                                   department_name=first_department_name, 
                                                                                                   avoid=avoid_matching_depatment_name) 

        departments = get_all_departments_with_page_ranges(valid_data, department_font_sizes, last_page)

#         print(departments,deprtment_dict_to_list(departments))

        #     if t.scraping_engine == 'pypdf2':
    #         data = df[df.filename == filename].pypdf2_detailed.iat[0]    

        courses = [
            (college, filename, department, course)
            for department, pages in departments.items()
            for course in get_courses(data, pages, regex_course_pattern)
        ]
        
        df_result = pd.DataFrame(courses, columns=['college','filename','department','course'])
        df_result = df_result.pipe(clear_junk_rows, college=college, filename=filename)
        final.append(df_result)
        

            
    
# df_final = 
pd.concat(final)

# if lame:= False:
#     with pd.ExcelWriter('data/ucla.xlsx') as writer:
#         df_final.to_excel(writer, 'data')
# else:
#     df_final['len'] = df_final.course.str.len()
# #     print('not uploaded', df_final[(df_final['len'] > 50000)])
#     df_final = df_final[~(df_final['len'] > 500)]
#     df_final.reset_index(inplace=True, drop=True)
#     df_final.drop(columns=['len','index'], inplace=True)
# #     print(df_final.head())
#     df2gsheet(df_final, college+'test') # TODO, e.g. df_result.at[255238,'course']
    """
    
    
 ### text_processing
    
# def get_all_departments_with_page_ranges(data, department_font_sizes, last_page) -> Dict:
#     """
#     returns mapping DEPARTMENT to PAGE_FROM:PAGE_TO, e.g.:
#     {
#         'AEROSPACE STUDIES –  AIR FORCE ROTC': {'from': 134, 'to': 138},
#         'AFRICAN STUDIES': {'from': 139, 'to': 139},
#         'AMERICAN INDIAN STUDIES': {'from': 140, 'to': 144},
#     }
#     """
#     max_dep_font_size = max(department_font_sizes)
#     departments = dict()
#     last_department = None
#     print(len(data))
#     for page in data:
#         for i,c in enumerate(page['characters']['size']):
#             if c == department_font_sizes:
#                 for j,cc in enumerate(page['characters']['size'][i:]):
#                     if cc not in department_font_sizes:
#                         break
#                 if j != 0:
#                     department = ''.join(page['characters']['chars'][i:i+j])
#                     if department.isspace(): 
#                         continue
#                     departments[department] = {'from': page['page'], 'to': None}
#                     if last_department:
#                         departments[last_department]['to'] = page['page'] - 1
#                     last_department = department
#                     j = 0
#                     break

#     departments[department]['to'] = last_page

#     return departments


# def get_departments(path, pages=27, department_font_size=17):
#     """ TODO """
#     department_courses = defaultdict(str)
#     department_name = ""
#     past_department_name = False

#     if c.size == department_font_size:
#         if past_department_name:
#             department_name = ""
#         department_name += c.get_text()
#         past_department_name = False
#     else:
#         past_department_name = True
#     department_courses[department_name] += obj.get_text()

#     return department_courses


# def get_char_list():
#     return


# def get_text_from_position(
#     data, page_id, index_from, index_to=None, how_long=None, chars=False
# ):
#     for page in data:
#         if page["page"] == page_id:
#             if index_to:
#                 till = index_to
#             if how_long:
#                 till = how_long + index_from
#             if chars:
#                 print(page["characters"]["size"][index_from:till])
#             return "".join(page["characters"]["chars"])[index_from:till]
        
        
# def strip_whitespace(s):
#     return s.replace('\n','').replace(' ','')


# def pop_two_lists_based_on_whitespace_index(text_list, other_list, other_other_list) -> Tuple[List,List]:
#     r1 = []
#     r2 = []
#     r3 = []
    
#     for i,(t,o,oo) in enumerate(zip(text_list,other_list,other_other_list)):
#         if t == ' ':
#             pass
#         elif t == '\n':
#             pass
#         else:
#             r1.append(t)
#             r2.append(o)
#             r3.append(oo)
#     return r1, r2, r3
       
    

# def pop_three_lists_based_on_whitespace_index(text_list, other_list, other_other_list) -> Tuple[List,List]:
#     r1 = []
#     r2 = []
#     r3 = []
    
#     for i,(t,o,oo) in enumerate(zip(text_list,other_list,other_other_list)):
#         if t == ' ':
#             pass
#         elif t == '\n':
#             pass
#         else:
#             r1.append(t)
#             r2.append(o)
#             r3.append(oo)
#     return r1, r2, r3

    

# def find_department_font(page, department_name, avoid=None) -> Tuple[List,List]:
#     """
#     TODO: better to use regex here
#     """
# #     chars, sizes = pop_two_lists_based_on_whitespace_index(page['characters']['chars'],page['characters']['size'])
#     chars, sizes, fonts = pop_three_lists_based_on_whitespace_index(page['characters']['chars'],
#                                                                     page['characters']['size'],
#                                                                     page['characters']['fontfamily'])
    
#     department_name = regex_pattern_ignore_whitespace(department_name)
#     page_text = ''.join(page['characters']['chars'])
# #     page_text = strip_whitespace(''.join(chars))
#     f = re.search(pattern=regex_pattern_ignore_whitespace(department_name),
#               string=page_text)
#     print(f)
#     if avoid:
#         avoid_index = page_text.index(strip_whitespace(avoid))
#         page_text = page_text[avoid_index+1:]
#         chars = chars[avoid_index+1:]
#     try:
#         dep_index = page_text.index(department_name)
#         dep_len = len(department_name)
#         dep_font_size = sizes[dep_index:dep_index+dep_len]
#         dep_font_family = fonts[dep_index:dep_index+dep_len]
#         txt_font_size = sizes[dep_index-1 : 1+dep_index+dep_len : dep_len+1]        
#     except ValueError:
#         print('ERROR\t',filename, college, first_page, last_page,'\n',department_name,'\n',page_text[:100])
    
#     return dep_font_size, dep_font_family, txt_font_size


# def get_all_departments(data, department_font_sizes, department_font_family, margin_of_error=0.1):
#     department_font_sizes.append(-1)
#     department_font_family.append(-1)
#     deps = []
#     for page in data:
#         r = ''
#         for c,s,f in zip(page['characters']['chars'], 
#                          page['characters']['size'], 
#                          page['characters']['fontfamily']):
#             if (math.isclose(max(department_font_sizes), s, abs_tol=margin_of_error) or
#                 math.isclose(min(department_font_sizes), s, abs_tol=margin_of_error) or
#                 int(s) == -1) and f in department_font_family:
#                 r += c
#             else:
#                 deps.append(r)
#                 r = ''
#     return deps
    



