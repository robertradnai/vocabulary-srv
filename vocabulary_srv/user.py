from random import randint

import jwt
import uuid
import datetime


class GuestUser:
    def __init__(self, id: str, expires: str):
        self.id: str = id
        self.expires = expires

    def get_jwt(self, secret_key) -> str:
        return jwt.encode(self.get_jwt_body(), secret_key, algorithm='HS256')

    def get_jwt_body(self) -> dict:
        return {"guestUserId": self.id, "expires": self.expires}


class GuestUserFactory:
    @staticmethod
    def generate() -> GuestUser:
        expires_at = (datetime.datetime.now().replace(microsecond=0)
                      + datetime.timedelta(hours=2))
        return GuestUser(str(uuid.uuid1()), expires_at.isoformat())

    @staticmethod
    def from_jwt(jwt_string: str, secret_key: str) -> GuestUser:
        decoded_body = jwt.decode(jwt_string, secret_key, algorithms=['HS256'])
        return GuestUser(decoded_body["guestUserId"], decoded_body["expires"])
