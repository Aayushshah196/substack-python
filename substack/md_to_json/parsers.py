from abc import ABC, abstractmethod
from functools import singledispatch
from typing import List, Optional

import markdown
from bs4 import BeautifulSoup, Tag
from loguru import logger

from .inline_parser import parse_inline_elements
from .structures import Attrs, Content, Document


class ElementParser(ABC):
    @abstractmethod
    def parse(self, element: Tag) -> Optional[Content]:
        pass


class HeadingParser(ElementParser):
    def parse(self, element: Tag) -> Optional[Content]:
        level = int(element.name[1])
        return Content(
            type="heading",
            attrs=Attrs(level=level),
            content=[Content(type="text", text=element.text)],
        )


class ParagraphParser(ElementParser):
    def parse(self, element: Tag) -> Optional[Content]:
        return Content(type="paragraph", content=parse_inline_elements(element))


class ListParser(ElementParser):
    def parse(self, element: Tag) -> Optional[Content]:
        list_type = "bullet_list" if element.name == "ul" else "ordered_list"
        attrs = Attrs(start=1, order=1) if list_type == "ordered_list" else None
        return Content(
            type=list_type,
            attrs=attrs,
            content=[parse_element(li) for li in element.find_all("li", recursive=False)],
        )


class ListItemParser(ElementParser):
    def parse(self, element: Tag) -> Optional[Content]:
        return Content(
            type="list_item",
            content=[parse_element(child) for child in element.children if child.name],
        )


class ImageParser(ElementParser):
    def parse(self, element: Tag) -> Optional[Content]:
        return Content(
            type="captionedImage",
            content=[
                Content(
                    type="image2",
                    attrs=Attrs(src=element.get("src"), alt=element.get("alt")),
                )
            ],
        )


class ParserFactory:
    @staticmethod
    def get_parser(element_name: str) -> ElementParser:
        parsers = {
            "h1": HeadingParser(),
            "h2": HeadingParser(),
            "p": ParagraphParser(),
            "ul": ListParser(),
            "ol": ListParser(),
            "li": ListItemParser(),
            "img": ImageParser(),
        }
        return parsers.get(element_name)


@singledispatch
def parse_element(element) -> Optional[Content]:
    return None


@parse_element.register
def _(element: Tag) -> Optional[Content]:
    parser = ParserFactory.get_parser(element.name)
    return parser.parse(element) if parser else None


# def parse_inline_elements(element: Tag) -> List[Content]:
#     content = []
#     for child in element.children:
#         if isinstance(child, str):
#             content.append(Content(type="text", text=child))
#         elif child.name == "strong":
#             content.append(
#                 Content(type="text", text=child.text, marks=[Mark(type="strong")])
#             )
#         elif child.name == "em":
#             content.append(
#                 Content(type="text", text=child.text, marks=[Mark(type="em")])
#             )
#         elif child.name == "a":
#             content.append(
#                 Content(
#                     type="text",
#                     text=child.text,
#                     marks=[Mark(type="link")],
#                     attrs=Attrs(
#                         href=child.get("href"),
#                         target="_blank",
#                         rel="noopener noreferrer nofollow",
#                     ),
#                 )
#             )
#     return content


def markdown_to_json(markdown_text: str) -> Document:
    markdown_text = "\n".join([line.strip() for line in markdown_text.split("\n") if line.strip()])
    html = markdown.markdown(markdown_text)
    soup = BeautifulSoup(html, "html.parser")
    document = Document(content=[])

    for element in soup.children:
        logger.info(f"Processing element: {element} | {type(element)} | {element.name}")
        if isinstance(element, Tag):
            content = parse_element(element)
            if content:
                document.content.append(content)
        elif element.name:
            content = parse_element(element)
            if content:
                document.content.append(content)

    return document


def remove_none_values(obj):
    if isinstance(obj, dict):
        return {key: remove_none_values(value) for key, value in obj.items() if value is not None}
    elif isinstance(obj, list):
        return [remove_none_values(item) for item in obj if item is not None]
    else:
        return obj


if __name__ == "__main__":
    # Example usage
    markdown_text = """
    ## Hello world

    This is a **test** [Hello world](https://example.com)

    - Hello world
    1. world

    [Hello world](https://example.com)

    ![Image](https://example.com/image.jpg)
    """

    document = markdown_to_json(markdown_text)
    cleaned_document = remove_none_values(document.model_dump())
    print(cleaned_document)
