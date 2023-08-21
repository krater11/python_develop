import secrets

import jwt


def generate_token(username, password):
    # 设置密钥，用于签名和验证令牌

    # 构建 payload，可以包含任意自定义的数据
    payload = {
        'username': username,
        'password': password
    }

    # 生成令牌
    SECRET_KEY = secrets.token_hex(64)

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return token
