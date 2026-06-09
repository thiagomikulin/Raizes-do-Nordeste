from fastapi import Depends

from datetime import datetime, timedelta, timezone
from main import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from jose import jwt


def criar_token(id, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc)+duracao_token
    dict_info = {
        "sub":str(id),
        "exp":data_expiracao
    }
    print(type(SECRET_KEY))
    encoded_jwt =jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    #JWT
    #ID
    #data_expiracao #passou desse período, tem que gerar um novo
    return encoded_jwt
