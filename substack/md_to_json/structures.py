from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class Attrs(BaseModel):
    level: Optional[int] = None
    href: Optional[str] = None
    target: Optional[str] = None
    rel: Optional[str] = None
    class_: Optional[str] = Field(None, alias="class")
    start: Optional[int] = None
    order: Optional[int] = None
    src: Optional[str] = None
    srcNoWatermark: Optional[str] = None
    fullscreen: Optional[bool] = None
    imageSize: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None
    resizeWidth: Optional[int] = None
    bytes: Optional[int] = None
    alt: Optional[str] = None
    title: Optional[str] = None
    type: Optional[str] = None
    belowTheFold: Optional[bool] = None
    topImage: Optional[bool] = None
    internalRedirect: Optional[str] = None


class Mark(BaseModel):
    type: str


class Content(BaseModel):
    type: str
    text: Optional[str] = None
    marks: Optional[List[Mark]] = None
    attrs: Optional[Attrs] = None
    content: Optional[List["Content"]] = list()

    def add(self, content: "Content"):
        if not self.content:
            self.content = []
        self.content.append(content)

    def model_dump(self, *args, **kwargs):
        return self.model_dump(*args, **kwargs)

    def add_paragraph(self, text: str):
        self.add(Content(type="paragraph", content=[Content(type="text", text=text)]))

    def add_heading(self, text: str, level: int):
        self.add(
            Content(
                type="heading",
                content=[Content(type="text", text=text)],
                attrs=Attrs(level=level),
            )
        )


Content.model_rebuild()


class Document(BaseModel):
    type: str = "doc"
    content: List[Content]

    @classmethod
    def create_empty_document(self):
        content = [Content(type="paragraph", content=[Content(type="text", text="")])]
        return Document(content=content)

    def add(self, content: Content):
        self.content.append(content)
