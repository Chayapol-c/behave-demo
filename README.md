# Final V&V

## Gherkin Keyword ที่ควรรู้เพื่ม

- [`Scenario outline`](https://cucumber.io/docs/gherkin/reference/#scenario-outline )
ใช้สำหรับ รัน `Scenario` หลายๆครั้ง 

- [`Example`](https://cucumber.io/docs/gherkin/reference/#examples)
เปน keyword ที่มาคู่กับ Scenario outline ใช้สำหรับระบุ test suites โดยจะทำเปน`Data table`ในแต่ละ row จะเปน input

- [`Data table`](https://cucumber.io/docs/gherkin/reference/#data-tables)
```Gherkins
  | name   | email              | twitter         |
  | Aslak  | aslak@cucumber.io  | @aslak_hellesoy |
  | Julien | julien@cucumber.io | @jbpros         |
  | Matt   | matt@cucumber.io   | @mattwynne      |
```

## การใช้งาน Behave
Behave เหมือนกับ Cucumber ใช้สำหรับทำ BDD โดยการรัน Gherkin ใน ไฟล์ `.feature`

ลง behave ด้วย pip
```
pip install behave
```


รัน test
```console
behave
```
หรือ
```console
behave ./[feature_file_path]
```

การเริ่มต้นสร้าง step ให้สร้างไฟล์ python ขึ้นมา

เรียกใช้งาน behave
```python
from behave import *
```

สร้าง function สำหรับรัน test (ใช้เปน unittest ก้ดี)
```python
@given('some other known state')
def step_impl(context):
    set_up(some, other, state)
```
- ตัว anotation จะตรงกับ ใน `.feature` ยกเว้น And จะไม่มี @and จะใช้ @then แทน
- context เปน param พิเศษซึ่งสามารถนำไปใน subsequent อื่นใน step เดียวกันได้   
e.g.
```
context.response = "abc"
```
statement ข้างบนจะเปนการสร้าง **key** response ที่เก็บ **value** "abc"
```python
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
```
จากชุดคำสั่งข้างต้น context.email และ context.name จะเก็บค่าที่ GET มาจาก `user_url` และจำสามารถเรียกใช้งานต่อได้ใน @then @then


ถ้าได้ลองสร้าง step ด้วย behave จะพบกับปัญหานึง นั่นคือ print() ของ python จะไม่ถูกแสดงออกมา ซึ่งต้องสร้างไฟล์ `behave.ini` ไว้ที่ directory นอกสุด
```
[behave]
stderr_capture=False
stdout_capture=False
```
และการที่จะ print() สิ่งใดออกมาจะต้องมีการเว้นบรรทัดต่อท้ายเสมอ print() ไม่ก้ \n

## Github APIs
สิ่งแรกที่ต้องมีสำหรับการใช้งานคือ Access Token หลังจากได้ access token มาก้ในไปใส่ใน .env 
```
pip install dotenv
```
การเรียกใช้ env
```python
from dotenv import load_dotenv
import os

load_dotenv()
access_token = os.getenv("GITHUB_ACCESS_TOKEN") # key ชื่อ GITHUB_ACCESS_TOKEN
```
การส่ง access token ในการใช้งาน API
```python
res = requests.post(repos_url, headers={'Authorization': 'token {}'.format(access_token)})
```

endpoint สำหรับ user(ไม่ต้องใส่ auth)
```
https://api.github.com/users/[user_name]
```
endpoint สำหรับ repository 
```
https://api.github.com/user/repos
```
รู้สึกเหมือนว่าถ้าใส่ Access token ไป มันจะเหมือนเรา login เข้าไปใน Github แล้วจัดการกับ repos ของเรา

e.g. สร้าง repoของเราใหม่
```python
data = {
        "name": "blog", 
        "auto_init": True, 
        "private": True, 
        "gitignore_template": "nanoc" 
}

res = requests.post(repos_url, headers={'Authorization': 'token {}'.format(access_token)}, json=data)
```