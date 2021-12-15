from behave import given, when, then
import requests
from dotenv import load_dotenv
import os

load_dotenv()

base_url = "https://api.github.com/users/"
@given("I am an authenticated user")
def test_step_impl(context):
    access_token = os.getenv("GITHUB_ACCESS_TOKEN")
    context.token= access_token


@when(u'I query the user data for "{username}"')
def test_step_impl(context, username: str):
    user_url = f"{base_url}{username}"
    res = requests.get(user_url, headers={'Authorization': 'token {}'.format(context.token)})
    data = res.json()
    context.email = data["email"]
    context.name = data["name"]

@then(u"the email is {email}")
def test_step_impl(context, email:str):
    if not context.email: 
        context.email = "null"
    assert context.email == email 

@then(u'the name is {name}')
def test_step_impl(context, name: str):
    if '"' in name: 
        name = name.strip('"')
    assert context.name == name