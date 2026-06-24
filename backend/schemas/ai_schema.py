from pydantic import BaseModel


class AiModel(BaseModel):
    context: str
    question: str


class AiAnswerModel(BaseModel):
    context: str
    question: str
    answer: str
