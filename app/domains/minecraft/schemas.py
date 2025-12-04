from pydantic import BaseModel


class User(BaseModel):
    nickname: str
    name: str
    course: int
    faculty: str
    nbook: int
