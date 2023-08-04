# Dira Abinawa

## GET STARTED
```bash
git clone https://github.com/Dira-Abinawa/Dira-Abinawa.git
```

## After Cloning

``` Bash
Python -m virtualenv env
env/Scripts/activate
```

After activating it you can install the package by running the following code :
```bash
pip install pymongo
pip install pydantic
pip install fastapi
pip install passlib
pip install bcrypt
pip install python-jose
```

## Running
```bash
uvicorn main:app --reload
```

## Level in Dewan Kerja Ranting
#### 1. `Bantara` 
#### 2. `Laksana` 
#### 3. `Garuda` 
    
Sure, here is a README.md that includes the endpoints from the code:



## Login User
#### User
    Username : johndoe
    Password : secret
#### Admin
    Username : admin
    Password : admin


### Endpoints

| Endpoint | Description | Authentication |
|---|---|---|
| `/token/` | This endpoint allows users to login. | Admin & User |
| `/token/register` | This endpoint allows users to register a new account. | No authentication required. |
| `/token/users/me/` | This endpoint returns the current user's data. | Admin & User |
| `/token/user/all` | This endpoint returns all users data. | Admin only. |

## Dewan Kerja Ranting
### Endpoints

| Endpoint | Method | Description | Authentication |
| --- | --- | --- | --- |
| `/dkr` | `GET` | Get all DKRs. | No authentication required. |
| `/dkr` | `POST` | Create a new DKR. | Admin only. |
| `/dkr/{id}` | `GET` | Get the DKR with the given ID. | Admin only. |
| `/dkr/{id}` | `PUT` | Update the DKR with the given ID. | Admin only. |
| `/dkr/{id}` | `DELETE` | Delete the DKR with the given ID. | Admin only. |

## School in Padalarang
### Endpoints

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| GET | /schools | Get a list of all schools. | No authentication required. |
| POST | /schools | Create a new school. | Admin only. |
| PUT | /schools/<id> | Update an existing school. | Admin only. |
| DELETE | /schools/<id> | Delete a school. | Admin only. |

## Data Potensi
### Endpoints

| Method | Endpoint | Description | Authentication|
|---|---|---|---|
| GET | /dapot | Get a list of all data potensi. | No authentication required. |
| POST | /dapot | Create a new data potensi. | Admin only. |
| PUT | /dapot/<id> | Update an existing data potensi. | Admin only. | 
| DELETE | /dapot/<id> | Delete a data potensi. | Admin only. |

## News
### Endpoints

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| `GET` | `/news` | Get a list of all news. | No authentication required. |
| `POST` | `/news` | Create a new news. | Admin only. |
| `GET` | `/news/hashtag` | Get news by hashtag. | No authentication required. |
| `PUT` | `/news/<id>` | Update a news. | Admin or author only. |
| `DELETE` | `/news/<id>` | Delete a news. | Admin or author only. |

## Comments
### Endpoints

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| `GET` | `/coment` | Get all comments for the current user. | No authentication required. |
| `GET` | `/coment/by_news/{id_news}` | Get comments for a specific news. | No authentication required. |
| `POST` | `/coment/` | Create a new comment. |  Admin or author only. |
| `PUT` | `/coment/<id>` | Update a comment. |  Admin or author only. |
| `DELETE` | `/coment/<id>` | Delete a comment. |  Admin or author only. |

## Activity
### Endpoints

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| `GET` | `/activity` | Get a list of all activities. | No authentication required. |
| `POST` | `/activity/` | Create a new activity. | Admin only. |
| `PUT` | `/activity/<id>` | Update an activity. | Admin only. |
| `DELETE` | `/activity/<id>` | Delete an activity. | Admin only. |

## Opinion
### Endpoints

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| `GET` | `/opinion` | Get a list of all opinions. | No authentication required. |
| `POST` | `/opinion/` | Create a new opinion. | Only authenticated users. |
| `PUT` | `/opinion/<id>` | Update an opinion. | Only authenticated users who created the opinion. |
| `DELETE` | `/opinion/<id>` | Delete an opinion. | Only authenticated users who created the opinion. |