import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from tada.src.api.models import Status


class ArticlePayload(BaseModel):
    title: str
    content: str
    status: Optional[Status] = Status.DRAFT


class ArticleResponse(ArticlePayload):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
