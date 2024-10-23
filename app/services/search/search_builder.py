from app.services.search.parsers.ridet import is_ridet
from app.services.search.queries.search_by_ridet import search_by_ridet
from app.services.search.queries.search_by_text import search_by_text


def build_search(search_build):
    query_terms = search_build.search_params.terms
    print("build search query_terms", query_terms)

    if is_ridet(query_terms):
        print("build search is ridet : ")
        search_build.search_client = search_by_ridet(query_terms)
    else:
        print("build search is text : ")
        search_build.search_client = search_by_text(search_build.search_params)
