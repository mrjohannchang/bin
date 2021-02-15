#!/usr/bin/env python3

import argparse
import html.parser
from typing import List, Tuple
import urllib.request


class AixdzsHTMLParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.last_url: str = ''
        self.next_url: str = ''

        self.is_in_content_tag: bool = False
        self.content_tag_nested_count: int = 0
        self.content: str = ''

        self.is_in_episode_name_tag: bool = False
        self.episode_name_tag_nested_count: int = 0
        self.episode_name: str = ''

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str]]):
        attr: Tuple[str, str]
        if tag == 'a':
            for attr in attrs:
                if attr[0] != 'href':
                    continue
                self.last_url = attr[1]
        elif tag == 'div':
            if self.is_in_content_tag:
                self.content_tag_nested_count += 1
            for attr in attrs:
                if attr[0] != 'class':
                    continue
                if attr[1] == 'content':
                    self.is_in_content_tag = True
        elif tag == 'h1':
            if self.is_in_episode_name_tag:
                self.episode_name_tag_nested_count += 1
            else:
                self.is_in_episode_name_tag = True

    def handle_endtag(self, tag: str):
        if tag == 'div':
            if self.content_tag_nested_count > 0:
                self.content_tag_nested_count -= 1
                return
            if self.is_in_content_tag:
                self.is_in_content_tag = False
        elif tag == 'h1':
            if self.episode_name_tag_nested_count > 0:
                self.episode_name_tag_nested_count -= 1
                return
            if self.is_in_episode_name_tag:
                self.is_in_episode_name_tag = False

    def handle_data(self, data: str):
        if data == '下一章[→]':
            self.next_url = self.last_url
        elif self.is_in_content_tag:
            self.content += data
        elif self.is_in_episode_name_tag:
            self.episode_name = data
            self.content += '\n' + self.episode_name + '\n'


class TxtDownloader:
    def __init__(self, begin_url: str, num_of_episodes_to_get: int):
        self.begin_url: str = begin_url
        self.episode_urls: List[str] = list()
        self.num_of_episodes_to_get: int = num_of_episodes_to_get
        self.content: str = ''

    def start(self):
        current_url: str = self.begin_url

        for _ in range(self.num_of_episodes_to_get):
            page: str = urllib.request.urlopen(current_url).read().decode()
            aixdzs_html_parser: AixdzsHTMLParser = AixdzsHTMLParser()
            aixdzs_html_parser.feed(page)
            self.content += aixdzs_html_parser.content
            if not aixdzs_html_parser.next_url:
                break
            current_url = urllib.parse.urljoin(self.begin_url, aixdzs_html_parser.next_url)
            self.episode_urls.append(current_url)


def parse_args() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description='Download episodes from 愛下電子書 https://tw.aixdzs.com/')
    parser.add_argument('begin_url', help='the URL of the begin episode')
    parser.add_argument('number_of_episodes', type=int, help='the number of the episodes to download')
    return parser.parse_args()


args: argparse.Namespace = parse_args()
tdler: TxtDownloader = TxtDownloader(args.begin_url, args.number_of_episodes)
tdler.start()
print(tdler.content)
