import requests
from dotenv import load_dotenv
import os

load_dotenv()
access_token = os.getenv("GITHUB_ACCESS_TOKEN")

base_url = "https://api.github.com/users/chayapol-c"
repos_url = "https://api.github.com/user/repos"
issues_url = "https://api.github.com/issues"

data = {
        "name": "blog", 
        "auto_init": True, 
        "private": True, 
        "gitignore_template": "nanoc" 
}

# res = requests.post(repos_url, headers={'Authorization': 'token {}'.format(access_token)}, json=data)
# print(res.json())

res = requests.get("https://api.github.com/user", headers={'Authorization': 'token {}'.format(access_token)})
print(res.json())