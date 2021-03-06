# -*- coding: utf-8 -*-
# @Time    : 2021/2/21 17:50
# @Author  : sunnysab
# @File    : __init__.py

from typing import List, Tuple

import scrapy


def filter_links(link_list: List[Tuple]) -> List[Tuple]:
    """
    Filter links which starts with 'javascript:' and so on.
    :param link_list: Original list to filter.
    :return: A filtered link list.
    """
    forbidden_link_prefix_set = {
        # Some are from https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/a
        '#', 'javascript:', 'mailto:', 'file:', 'ftp:', 'blob:', 'data:'
    }

    def is_forbidden_url(url: str) -> bool:
        for prefix in forbidden_link_prefix_set:
            if url.startswith(prefix):
                return True
        return False

    return [(title, url) for title, url in link_list if not is_forbidden_url(url)]


def get_links(response: scrapy.http.Response) -> List[Tuple[str or None, str]]:
    """
    Get links in the page.
    :param response: A scrapy.http.Response that contains the page
    :return: A list of tuple (title, url)
    """
    link_list = [(a_node.xpath('.//text()').get(), a_node.attrib['href'])  # Make a tuple of title, href
                 for a_node in response.css('a[href]')]
    return filter_links(link_list)


def guess_link_type(path: str) -> str:
    """
    Guess link type by path
    :param path: Path in url.
    :return: 'page' if it seems like a page.
             'attachment' if it seems like an attachment.
             'unknown' if we don't know.
    """

    page_postfix_set = {
        'asp', 'aspx', 'jsp', 'psp', 'do', 'htm', 'html', 'php', 'cgi', '/', 'portal', 'action'
    }

    attachment_postfix_set = {
        # '7z', 'zip', 'rar',
        'xls', 'xlsx', 'doc', 'docx', 'ppt', 'pptx', 'pdf'
    }

    for each_postfix in page_postfix_set:
        if path.endswith(each_postfix):
            return 'page'

    for each_postfix in attachment_postfix_set:
        if path.endswith(each_postfix):
            return 'attachment'

    return 'unknown'
