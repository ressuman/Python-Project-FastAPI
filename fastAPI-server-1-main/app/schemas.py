from pydantic import BaseModel, HttpUrl

from typing import Sequence


class User(BaseModel):
    id: int
    name: str
    email: str


class Recipe(BaseModel):
    id: int
    label: str
    source: str
    url: HttpUrl
    user_id: int
    is_public: bool


class RecipeSearchResults(BaseModel):
    results: Sequence[Recipe]


class RecipeCreate(BaseModel):
    label: str
    source: str
    url: HttpUrl
    submitter_id: int
