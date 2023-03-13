
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

def easy_find_all_pages(paragraphs, total_pages):
    pages_found = []
    page_number_loc = []
    page_loc = 0
    page = 1
    while True:
        check_page_loc = page_loc
        page, page_loc, found = (find_page(paragraphs[page_loc:page_loc + 30], total_pages, page=page, start_page_loc=page_loc))
        if found:
            pages_found.append(page)
            page_number_loc.append(page_loc)
        page += 1
        if page_loc == check_page_loc:
            break
    return pages_found, page_number_loc

