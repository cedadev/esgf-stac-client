from pystac_client import Client
from typing import Iterator, List, Optional
from pystac import Collection
from enum import Enum
from pystac_client.item_search import BBoxLike, DatetimeLike, FilterLike, FilterLangLike, FreeTextLike, CollectionsLike,\
    DEFAULT_LIMIT_AND_MAX_ITEMS, QueryLike, IntersectsLike, SortbyLike, FieldsLike, IDsLike
from pystac_client.asset_search import ItemsLike

class ESGFStacClient(Client):

    def get_collection_list(self) -> List:
        collections: Iterator[Collection] = super().get_collections()
        return [collection for collection in collections]

    def search(self,
               doctype: str = "items",
               method: Optional[str] = "GET",
               limit: Optional[int] = DEFAULT_LIMIT_AND_MAX_ITEMS,
               max_items: Optional[int] = DEFAULT_LIMIT_AND_MAX_ITEMS,
               ids: Optional[IDsLike] = None,
               collections: Optional[CollectionsLike] = None,
               bbox: Optional[BBoxLike] = None,
               intersects: Optional[IntersectsLike] = None,
               datetime: Optional[DatetimeLike] = None,
               query: Optional[QueryLike] = None,
               filter: Optional[FilterLike] = None,
               filter_lang: Optional[FilterLangLike] = None,
               sortby: Optional[SortbyLike] = None,
               fields: Optional[FieldsLike] = None,
               q: Optional[FreeTextLike] = None,
               source: Optional[List[str]] = None,
               **facets):

        if filter and facets:
            raise ValueError("'filter' parameter cannot be used in conjunction with facets.'"
                             "Please move facets into the filter string.")

        if facets:
            if method == "GET":
                filter = self._get_format_facets(**facets)
            elif method == "POST":
                filter = self._post_format_facets(**facets)

        if doctype == "items" or doctype == "datasets":
            return super().search(
                method=method,
                max_items=max_items,
                limit=limit,
                ids=ids,
                collections=collections,
                bbox=bbox,
                intersects=intersects,
                datetime=datetime,
                query=query,
                filter=filter,
                filter_lang=filter_lang,
                sortby=sortby,
                fields=fields,
                q=q,
                source=source
            )
        elif doctype == "assets" or doctype == "files":
            if collections:
                raise ValueError(f"parameter 'collections' is for item search. Doctype {doctype} specified.")
            return super().asset_search(
                method=method,
                limit=limit,
                ids=ids,
                bbox=bbox,
                intersects=intersects,
                datetime=datetime,
                query=query,
                filter=filter,
                filter_lang=filter_lang,
                sortby=sortby,
                q=q,
            )

    @staticmethod
    def _get_format_facets(**facets) -> str:
        filter_string = ''
        for key, value in facets.items():
            if isinstance(value, str):
                filter_string = f"{filter_string}{key} = '{value}' and "
            elif isinstance(value, list):
                list_query = ''
                for item in value:
                    list_query = f"{list_query}{key} = '{item}' or "
                filter_string = f"{filter_string}({list_query.rstrip(' or ')}) and "
            else:
                raise ValueError(f"facet encountered invalid datatype: {type(value)} for facet kwarg: {key}")
        return filter_string.rstrip(' and ')

    @staticmethod
    def _post_format_facets(**facets) -> dict:
        filter_list = []

        for facet, value in facets.items():
            if isinstance(value, str):
                filter_list.append(
                    {"eq": [{"property": facet}, value]}
                )
            elif isinstance(value, list):
                filter_list.append(
                    {"or": [
                        {"eq": [{"property": facet}, v]} for v in value
                    ]}
                )
        return {"and": filter_list}


