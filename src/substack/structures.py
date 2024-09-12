import json
from datetime import datetime
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, HttpUrl

from substack.md_to_json.structures import Document


class Publication(BaseModel):
    id: int
    name: str
    subdomain: str


class PublicationUser(BaseModel):
    user_id: int
    publication_id: int
    role: str
    publication: Publication = Field(alias="publication")


class PublishedByline(BaseModel):
    id: int
    name: str
    handle: str
    photo_url: Optional[HttpUrl]
    publication_users: List[PublicationUser] = Field(alias="publicationUsers")


class Post(BaseModel):
    id: int
    publication_id: int
    title: str
    type: str
    slug: str
    post_date: datetime
    audience: str
    canonical_url: Optional[Union[str, HttpUrl]]
    subtitle: Optional[str]
    description: Optional[str]
    wordcount: int
    reactions: Dict[str, int]
    comment_count: int
    child_comment_count: int
    is_geoblocked: bool
    published_bylines: List[PublishedByline] = Field(alias="publishedBylines")
    has_cashtag: bool = Field(alias="hasCashtag")

    comments: Optional[list] = list()
    next_post_slug: Optional[str] = None
    body_html: Optional[str] = None
    body_json: Optional[str] = None
    previous_post_slug: Optional[str] = None
    publication_name: Optional[str] = None
    publication_subdomain: Optional[str] = None

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}

    @classmethod
    def from_dict(cls, orig_data: dict) -> "Post":
        import copy

        data = copy.deepcopy(orig_data)
        if isinstance(data.get("post_date"), str):
            data["post_date"] = datetime.fromisoformat(data["post_date"].rstrip("Z"))

        if "publishedBylines" in data:
            bylines = []
            for byline in data["publishedBylines"]:
                if "publicationUsers" in byline:
                    for pub_user in byline["publicationUsers"]:
                        if "publication" in pub_user:
                            publication = pub_user["publication"]
                            publication["publication_name"] = publication.get("name")
                            publication["publication_subdomain"] = publication.get("subdomain")
                bylines.append(PublishedByline(**byline))
            data["publishedBylines"] = bylines

        return cls(**data)

    @property
    def publication_url(self) -> Optional[str]:
        if self.publication_subdomain:
            return f"https://{self.publication_subdomain}.substack.com"
        return None


class DraftByline(BaseModel):
    id: int
    is_guest: bool


class Draft(BaseModel):
    type: str = "newsletter"
    audience: str = "everyone"
    draft_title: str = Field(..., alias="title")
    draft_subtitle: str = Field("", alias="subtitle")
    draft_body: Document = Field(..., default_factory=lambda: Document.create_empty_document())
    draft_bylines: List[DraftByline] = list()
    draft_section_id: Optional[str] = None
    draft_video_upload_id: Optional[None] = None
    section_chosen: bool = False

    def to_dict(self, body_json_dump=True):
        data = self.model_dump(exclude_none=True)
        data["draft_body"] = json.dumps(data["draft_body"]) if body_json_dump else data["draft_body"]
        return data
