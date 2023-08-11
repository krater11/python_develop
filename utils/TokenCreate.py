import secrets
import string


def generate_token(length=32):
    # 生成令牌所使用的字符集
    characters = string.ascii_letters + string.digits

    # 生成指定长度的令牌
    token = ''.join(secrets.choice(characters) for _ in range(length))

    return token