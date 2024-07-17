# Project Description
HTTP RESTful APIs for account and password management.

# Contents

- [Project Structure](#project-structure)
- [Solution Details](#solution-details)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Logging](#installation)
- [API Doc (Overview)](#api-doc-overview)

# Project Structure
Project Sturcture is followed by [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices#1-project-structure-consistent--predictable)

# Solution Details
- Impletmented two **RESTful APIs** for creating and verifying accounts and passwords.
- Used **Python** and **FastAPI** for backend development.
- Implemented **pydentic** for data validation. 
- Used **MySQL** for data storage.
- Used **Redis** for limiting the maximum retry count.
- Packed the solution in a **Docker image**, and pushed it to **Docker Hub**.
- Implemented **pytest** for unit tesing.
- Utilized **logging** to record critical and warning events, like Redis server down time and 429 too many request.
- Implemented **ruff** and **pre-commit** for consistent coding style.
- Created and maintained a API document using **Swagger UI**.

# Getting Started
The following instruction will let you deploy the auth-api project on your local machine by Docker Container.

## Prerequistites
Before you begin, please make sure you have the following installed on your machine:
- **Git:** for cloning this project
- **Docker:** for building and running a container

## Installation
### 1. Clone the repository
Cloning this repository to your local machine.
```
git clone https://github.com/sophie0730/auth-api.git
```

### 2. Set the environment variable
We only use `.prod.env` for demonstraing this project. You don't need to change any data in this file since they are used for demonstrating only.
```
cd auth-api
mv .prod.env.example .prod.env
```

### 3. Run the container
There are two versions of the image for different CPU architectures: `linux/amd` and `linux/arm`. Your local machine will choose the suitable version and pull it automatically.
```
docker compose up -d
```
### 4. Navigate API Document
You can navigate the API Document for reference of the following tests.
```
http://localhost:8000/docs
```
 
### 5. Test by CLI: POST a request for signing up
```
curl -X POST \
-H "Content-Type: application/json" \
-d '{
        "username": "sophie",
        "password": "Asd123456"
    }' \
http://localhost:8000/api/v1/signup
```
### 6. Test by CLI: POST a request for signing in
```
curl -X POST \
-H "Content-Type: application/json" \
-d '{
        "username": "sophie",
        "password": "Asd123456"
    }' \
http://localhost:8000/api/v1/signin
```

### 7. All tests are done. Stop all containers.
Please notice that `-v` will remove all volumes.
```
docker compose down -v
```

## Logs
This project utilizes the `logging` module to record critical and warning level events. Logs are generated for events such as:
- Redis server downtime 
- 429 too many requests 

**Notes:** The logs are generated inside the container but are stored in local storage `<your-repo-path>/logs_prod` for easier monitoring and data persistence.

# API Doc (Overview)
This section is an overview for these two RESTful API. For the detailed information, please refer to the Swagger API Document(http://localhost:8000/docs) after you run the container.


### API Version
1.0

### API 1: Create Account
* **End Point:**  `api/v1/user/signup`
* **Method:** `POST`
* **Request Headers:** 

| Field | Type | Description |
| :---: | :---: | :--- |
| Content-Type | String | Only accept `application/json`. |

* **Input: JSON Payload**

| Field | Type | Description |
| :---: | :---: | :--- |
| username | String | Required. 3~32 characters. |
| password | String | Required. 8~32 characters.  containing at least 1 uppercase letter, 1 lowercase letter, and 1 number

* **Output: JSON Payload**

| Field | Type | Description |
| :---: | :---: | :--- |
| success | Boolean | The outcome of the account creation process. |
| reason | String | The reason for a failed account creation process. |


### API 2: Verify Account and Password
* **End Point:**  `api/v1/user/signin`
* **Method:** `POST`
* **Request Headers:** 

| Field | Type | Description |
| :---: | :---: | :--- |
| Content-Type | String | Only accept `application/json`. |

* **Input: JSON Payload**

| Field | Type | Description |
| :---: | :---: | :--- |
| username | String | Required. 3~32 characters. |
| password | String | Required. 8~32 characters.  containing at least 1 uppercase letter, 1 lowercase letter, and 1 number

* **Output: JSON Payload**

| Field | Type | Description |
| :---: | :---: | :--- |
| success | Boolean | The outcome of the account creation process. |
| reason | String | The reason for a failed account creation process. |
