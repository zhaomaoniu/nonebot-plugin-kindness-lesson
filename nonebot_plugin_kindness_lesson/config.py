from typing import Optional
from pydantic import BaseModel


class Config(BaseModel):
    kindness_lesson_model: str = "gpt-4o-mini"
    kindness_lesson_api_key: str
    kindness_lesson_base_url: Optional[str] = "https://api.openai.com/v1"
    kindness_lesson_proxy: Optional[str] = None
