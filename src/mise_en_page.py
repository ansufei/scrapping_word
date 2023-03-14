import re

def find_page(paragraphs, nb_pages, page=1, start_page_loc=0):
    found = 0
    page_loc = start_page_loc
    while (page_loc == start_page_loc) and (page < nb_pages):
        for i, par in enumerate(paragraphs):
            if par.text.isdigit() and int(par.text) == page:
                page_loc = i + start_page_loc
                found = 1
                break
        page += 1
    return page - 1, page_loc, found

def find_easy_page_numbers(doc, total_pages):
    result = {}
    page_loc = 0
    page = 1
    while True:
        check_page_loc = page_loc
        page, page_loc, found = (find_page(doc.paragraphs[page_loc:page_loc + 30], total_pages, page=page, start_page_loc=page_loc))
        if found:
            result[page] = page_loc
            doc.paragraphs[page_loc].text = 'page ' + str(page)
        page += 1
        if page_loc == check_page_loc:
            break
    return result

def narrow_location_hidden_page_numbers(first_page, total_pages, found_pages):
    # circumscribe location
    missing_pages = set(range(first_page,total_pages)) - set(found_pages.keys())
    missing = {}
    for page in missing_pages:
        # nearest found pages
        # before
        bef = [page - x for x in found_pages.keys() if x < page]
        bef_page = 0
        if len(bef) > 0:
            bef_page = found_pages[page - min(bef)]
        # after
        aft = [x - page for x in found_pages.keys() if x > page]
        aft_page = -1
        if len(aft) > 0:
            aft_page = found_pages[page + min(aft)]
        missing[page] = [bef_page,aft_page]
    return missing

def reformat_hidden_page_numbers(doc, hidden_pages_loc):
    still_missing = []
    for page in reversed(sorted(list(hidden_pages_loc.keys()))):
        missing_flag = True
        min_loc, max_loc = hidden_pages_loc[page]
        pars = [par for par in doc.paragraphs[min_loc:max_loc]]
        pattern_hidden = str(page) + r'(\s|$)'
        for par in pars:
            exact_loc = re.search(pattern_hidden, par.text)
            if not exact_loc is None:
                if par.text != str(page):
                    par.insert_paragraph_before(re.sub(pattern_hidden, '',par.text))
                par.text = 'page ' + str(page)
                par.paragraph_format.first_line_indent = None
                missing_flag = False
                break
        if missing_flag:
            still_missing.append(page)
            missing_flag = False
    return set(still_missing)