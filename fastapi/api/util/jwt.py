from dataclasses import dataclass
from jose import JWTError, jwt
import datetime as dt


@dataclass
class TokenData:
    sub: str
    exp: dt.datetime


@dataclass
class TokenFactory:
    secret_key: str
    duration = 30  # minutes
    algorithm: str = 'HS256'

    async def build(self, data: dict) -> str:
        expiration = dt.datetime.utcnow() + dt.timedelta(minutes=self.duration)
        to_encode = dict(exp=expiration, **data)
        return jwt.encode(claims=to_encode, key=self.secret_key, algorithm=self.algorithm)

    async def parse(self, token: str, raise_error: bool = False) -> TokenData:
        try:
            # TODO: check that token expiration is enforced
            payload = jwt.decode(token=token, key=self.secret_key, algorithms=[self.algorithm])
            return TokenData(sub=payload['sub'], exp=dt.datetime.fromtimestamp(payload['exp']))
        except JWTError as err:
            if raise_error:
                raise err


async def main():
    factory = TokenFactory(secret_key='abcdwxyz')
    token = await factory.build(dict(sub='person'))
    print(token)
    data = await factory.parse(token)
    print(data)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
