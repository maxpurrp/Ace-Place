from pydantic import BaseModel


class Notification(BaseModel):
    user_id: str
    target_id: str | None = None
    key: str
    data: dict | None = None


class ReadNotify(BaseModel):
    user_id: str
    notification_id: str


class Listing(BaseModel):
    user_id: str
    skip: int
    limit: int
