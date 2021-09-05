import datetime as dt
from dataclasses import asdict, dataclass, field
from typing import List

from jose import JWTError, jwt


@dataclass
class TokenData:
    sub: str
    exp: dt.datetime
    scopes: List[str] = field(default_factory=list)


@dataclass
class TokenFactory:
    secret_key: str
    duration = 30  # minutes
    algorithm: str = 'HS256'

    async def build(self, sub: str, scopes: List[str] = None) -> str:
        token_data = TokenData(
            sub=sub,
            exp=dt.datetime.utcnow() + dt.timedelta(minutes=self.duration),
            scopes=scopes or list()
        )
        return jwt.encode(claims=asdict(token_data), key=self.secret_key, algorithm=self.algorithm)

    async def parse(self, token: str, raise_error: bool = False) -> TokenData:
        try:
            payload = jwt.decode(token=token, key=self.secret_key, algorithms=[self.algorithm])
            return TokenData(sub=payload['sub'], exp=dt.datetime.fromtimestamp(payload['exp']))
        except JWTError as err:
            if raise_error:
                raise err
