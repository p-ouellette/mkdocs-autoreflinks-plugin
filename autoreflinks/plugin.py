from mkdocs.plugins import BasePlugin
from markdown.extensions.toc import slugify
from bs4 import BeautifulSoup
import re


def top_level_text(tag):
    return tag.name in ['p', 'li'] and not tag.find_parent('li')


class AutoRefLinks(BasePlugin):

    def on_nav(self, nav, **kwargs):
        self.pages = []
        for page in nav.pages:
            with open(page.file.abs_src_path, 'r') as file:
                self.pages.append((page, file.read()))

    def get_heading_url(self, heading):
        for page, markdown in self.pages:
            if heading == page.title:
                return '/' + page.url
            h_regex = ' *{} *'.format(re.escape(heading))
            regex = re.compile('^{0}$\n^[=-]+$|^#+{0}$'.format(h_regex), re.M)
            if re.search(regex, markdown):
                return '/' + page.url + '#' + slugify(heading, '-')

    def on_page_content(self, html, **kwargs):

        def replace_bracketed_heading(match):
            heading = match[1].replace('<code>', '`').replace('</code>', '`')
            url = self.get_heading_url(heading)
            if url:
                return '<a href={}>{}</a>'.format(url, match[1])
            return match[0]

        soup = BeautifulSoup(html, 'html.parser')
        for tag in soup.find_all(top_level_text):
            tag_str = str(tag)
            new_str = re.sub(r'\[(.+?)\]', replace_bracketed_heading, tag_str)
            if new_str != tag_str:
                tag.replace_with(BeautifulSoup(new_str, 'html.parser'))
        return str(soup)
