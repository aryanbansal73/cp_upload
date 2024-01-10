from itsdangerous import URLSafeTimedSerializer

secret_key = "ghsighwosghsohg"
salt = "geiobeiaohgedhbdobhesojberohbnwebhngbeuwrghwa2r"

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(email, salt=salt)


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        email = serializer.loads(
            token,
            salt=salt,
            max_age=expiration
        )
    except:
        return False
    return email