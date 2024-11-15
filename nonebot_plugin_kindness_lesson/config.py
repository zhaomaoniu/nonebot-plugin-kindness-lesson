from typing import Optional
from pydantic import BaseModel


class Config(BaseModel):
    kindness_lesson_model: str = "gpt-4o-mini"
    kindness_lesson_api_key: str = "your-api-key"
    kindness_lesson_base_url: Optional[str] = "https://api.openai.com"
    kindness_lesson_proxy: Optional[str] = None
