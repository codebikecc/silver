from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param, remove_query_param


class LinkHeaderPagination(PageNumberPagination):
    def get_last_link(self):
        url = self.request.build_absolute_uri()
        page_number = self.page.paginator.num_pages
        return replace_query_param(url, self.page_query_param, page_number)

    def get_first_link(self, display_page_query_param=True):
        url = self.request.build_absolute_uri()
        if display_page_query_param:
            page_number = self.page.paginator.validate_number(1)
            return replace_query_param(url, self.page_query_param, page_number)
        else:
            return remove_query_param(url, self.page_query_param)

    def get_paginated_response(self, data):
        next_url = self.get_next_link()
        previous_url = self.get_previous_link()
        first_url = self.get_first_link()
        last_url = self.get_last_link()

        if next_url is not None and previous_url is not None:
            link = '<{next_url}; rel="next">, <{previous_url}; rel="prev">'
        elif next_url is not None:
            link = '<{next_url}; rel="next">'
        elif previous_url is not None:
            link = '<{previous_url}; rel="prev">'
        else:
            link = ''

        if link:
            link += ', '

        link += '<{first_url}; rel="first">, <{last_url}; rel="last">'

        link = link.format(next_url=next_url, previous_url=previous_url,
                           first_url=first_url, last_url=last_url)
        headers = {'Link': link} if link else {}

        return Response(data, headers=headers)