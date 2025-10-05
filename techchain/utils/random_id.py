import uuid, base64

def generate_user_id():
    uid = uuid.uuid4()
    return base64.urlsafe_b64encode(uid.bytes).rstrip(b'=').decode('utf-8')