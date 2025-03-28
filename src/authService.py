import datetime
from typing import Annotated
from fastapi import Header
import jwt

    
class Payload:
    id: str

    def __init__(self, id: str):
        self.id = id

class JwtService:

    secret: str

    def __init__(self, secret):
        self.secret = secret

    def sign(self, payload: Payload) -> str:
        dc = {}
        dc["id"] = payload.id
        dc["exp"] = datetime.datetime.now() + datetime.timedelta(minutes=30)
        return jwt.encode(dc, self.secret, algorithm='HS256')
    
    def validate(self, token: str) -> Payload:
        try:
            dc = jwt.decode(token, self.secret, algorithms=['HS256'])
            return Payload(dc["id"])
        except jwt.ExpiredSignatureError:
            return None

jwt_service = JwtService("secret")

def get_payload(authorization: Annotated[str, Header()]) -> Payload:
    token = authorization.split(" ")[1]
    return jwt_service.validate(token)
