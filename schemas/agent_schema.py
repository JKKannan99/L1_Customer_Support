from pydantic import BaseModel

class AgentLogin(BaseModel):
    username: str
    password: str

class AgentResponse(BaseModel):
    id: int
    username: str
    message: str

