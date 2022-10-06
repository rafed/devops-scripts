#!/usr/bin/python3

import requests
import json
from base64 import b64encode
from nacl import encoding, public

def encrypt(public_key: str, secret_value: str) -> str:
    """Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")

def get_public_key(gh_token, owner, repository, environment):
    url_public_key = f"https://api.github.com/repos/{owner}/{repository}/environments/{environment}/secrets/public-key"
    authorization = f"token {gh_token}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization" : f"token {gh_token}",
    }
    r = requests.get(url = url_public_key, headers = headers)
    
    if r.status_code != 200:
        print (r.status_code, r.reason)
        raise Exception("❌ Couldn't get the repository public key")
    
    response = r.json()
    key, key_id = response["key"], response["key_id"]
    return key, key_id

def upload_token(gh_token, owner, repository, environment, public_key, public_key_id, secret_name, secret_value):
    authorization = f"token {gh_token}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization" : authorization,
    }

    url_secret = f"https://api.github.com/repos/{owner}/{repository}/environments/{environment}/secrets/{secret_name}"

    data = {}
    data["encrypted_value"] = encrypt(public_key, secret_value)
    data["key_id"] = public_key_id

    json_data = json.dumps(data)

    r = requests.put(
        url = url_secret,
        data = json_data,
        headers = headers
    )

    if r.status_code == 201 or r.status_code == 204:
        print(f"✅ Secret \033[36m{secret_name}\033[0m successfully added to {owner}'s \033[36m{repository}\033[0m repository")
    else:
        raise Exception(f"❌ Couldn't add the secret {secret_name} to the repository")


token = ""
owner = ""
repository = ""
environment = ""

def put_secrets(from_file, environment):
    for line in open(from_file).read().splitlines():
        a = line.split("=", 1)

        key, key_id = get_public_key(token, owner, repository, environment)
        upload_token(token, owner, repository, environment, key, key_id, a[0], a[1])
        # print(a[0], a[1])
        
put_secrets(f"secrets_only/{environment}.env", environment)
