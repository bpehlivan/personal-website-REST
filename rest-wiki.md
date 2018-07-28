# API:
## 1. Login
Url: <host>/app/login
Method: POST
Body:
{
"username": "<username>",
"password": "<password>"
}
Header:
Content-Type: application/json
Response:
{
"token": "a7b3f6941d9876ba08d152527cf1105b01689afd"
}
## 2. Get Records
Url: <host>/app/getrecords/
Method: GET
Headers:
Authorization: Token <login token>
Response:
[
{
"user_id": 2,
"date": "2018-06-14",
"weight": 95,
"record_date": "2018-06-14T16:26:33+00:00"
},
....
]
## 3. Set Record
Url: <host>/app/record/
Method: POST
Headers:
Authorization: Token <login token>
Content-Type: application/json
Body:
{
"date": "<YYYY-DD-MM>",
"weight": <weight>,
"record time": "<YYYY-DD-MM HH:mm:SS+ZZ>"
}
Response:
if succesful:
{"response": "Success! your record saved!"}
else:
{“error”: “body could not be parsed”}
## 4. Delete Record
Url: <host>/app/record/
Method: DELETE
Headers:
Authorization: Token <login token>
Content-Type: application/json
Body:
{
"date": "<YYYY-DD-MM>"
}
Response:
if succesful:
{"response": "Success, your record deleted!"}
else:
{“error”: “body could not be parsed”}
## 5. Logout
Url: <host>/app/logout
Method: POST
Headers:Authantication: Token <login token>
no response
## 6. Register
Url: <host>/app/register
No authantication needed.
Headers:
Content-Type: application/json

Body:

{
"username": "<username>",
"email": "<email>",
"password": "<password>",
"first_name": "<first_name>",
"last_name": "<last_name>"
}

Response:
If success:

{
"response": "Success! User created!"
}

If username exists:

{
"response": "Fail! Username exists!"
}

If error happens:

{
"response": "Fail! Not registered!"
}
