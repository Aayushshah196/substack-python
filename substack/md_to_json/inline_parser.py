from functools import partial
from typing import Callable, Dict, List

from bs4 import NavigableString, Tag

from .structures import Attrs, Content, Mark


class InlineParserStrategy:
    @staticmethod
    def parse_text(element: NavigableString) -> Content:
        return Content(type="text", text=str(element))

    @staticmethod
    def parse_strong(element: Tag) -> Content:
        return Content(type="text", text=element.text, marks=[Mark(type="strong")])

    @staticmethod
    def parse_em(element: Tag) -> Content:
        return Content(type="text", text=element.text, marks=[Mark(type="em")])

    @staticmethod
    def parse_underline(element: Tag) -> Content:
        return Content(type="text", text=element.text, marks=[Mark(type="underline")])

    @staticmethod
    def parse_strikethrough(element: Tag) -> Content:
        return Content(type="text", text=element.text, marks=[Mark(type="strikethrough")])

    @staticmethod
    def parse_code(element: Tag) -> Content:
        return Content(type="text", text=element.text, marks=[Mark(type="code")])

    @staticmethod
    def parse_link(element: Tag) -> Content:
        return Content(
            type="text",
            text=element.text,
            marks=[Mark(type="link")],
            attrs=Attrs(
                href=element.get("href"),
                target="_blank",
                rel="noopener noreferrer nofollow",
            ),
        )

    @staticmethod
    def parse_quote(element: Tag) -> Content:
        return Content(type="text", text=element.text, marks=[Mark(type="quote")])


class InlineParser:
    def __init__(self):
        self.parser_map: Dict[str, Callable] = {
            "strong": InlineParserStrategy.parse_strong,
            "b": InlineParserStrategy.parse_strong,
            "em": InlineParserStrategy.parse_em,
            "i": InlineParserStrategy.parse_em,
            "u": InlineParserStrategy.parse_underline,
            "s": InlineParserStrategy.parse_strikethrough,
            "del": InlineParserStrategy.parse_strikethrough,
            "code": InlineParserStrategy.parse_code,
            "a": InlineParserStrategy.parse_link,
            "q": InlineParserStrategy.parse_quote,
        }

    def parse(self, element: Tag) -> List[Content]:
        content = []
        for child in element.children:
            if isinstance(child, NavigableString):
                content.append(InlineParserStrategy.parse_text(child))
            elif isinstance(child, Tag):
                parser = self.parser_map.get(child.name, self.parse_unknown)
                parsed_content = parser(child)
                if isinstance(parsed_content, list):
                    content.extend(parsed_content)
                else:
                    content.append(parsed_content)
        return content

    def parse_unknown(self, element: Tag) -> List[Content]:
        return self.parse(element)


def parse_inline_elements(element: Tag) -> List[Content]:
    parser = InlineParser()
    return parser.parse(element)
