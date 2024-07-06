## Project Description
HTTP RESTful APIs for account and password management.

## Contents

## Solution Details
- Impletmented two **RESTful APIs** for creating and verifying accounts and passwords.
- Used **Python** and **FastAPI** for backend development.
- Implemented **pydentic** for data validation. 
- Implemented **pytest** for unit tesing.
- Used **MySQL** for data storage.
- Used **Redis** for limiting the maximum retry count.
- Packed the solution in a **Docker image**, and pushed it to **Docker Hub**.
- Implemented **ruff** and **pre-commit** for consistent coding style.
- Used **GitHub Actions** for CI/CD.
- Created and maintained a API document using **Swagger UI**.

## Start


## API Doc (Overview)
This section is a overview for these two RESTful API. For the detailed information, please refer to the Swagger API Document after you run the container.


### API Version
1.0

### API 1: Create Account
* **End Point:**  `api/v1/user/signup`
* **Method:** `POST`
* **Request Headers:** 

| Field | Type | Description |
| :---: | :---: | :--- |
| Content-Type | String | Only accept `application/json`. |

* **Request Body: JSON Payload**

| Field | Type | Description |
| :---: | :---: | :--- |
| username | String | Required. 3~32 characters. |
| password | String | Required. 8~32 characters.  containing at least 1 uppercase letter, 1 lowercase letter, and 1 number

* **Success Response: 200 (JSON Payload)**

| Field | Type | Description |
| :---: | :---: | :--- |
| success | Boolean | Return True. The outcome of the account creation process. |
| reason | String | Return a empty string. The reason for a failed account creation process. |

* **Client Error Response: 400 (JSON Payload)**

| Field | Type | Description |
| :---: | :---: | :--- |
| success | Boolean | Return False. The outcome of the account creation process. |
| reason | String | The reason for a failed account creation process. |

* **Server Error Response: 500 (JSON Payload)**

| Field | Type | Description |
| :---: | :---: | :--- |
| success | Boolean | Return False. The outcome of the account creation process. |
| reason | String | The reason for a failed account creation process. |


### API 2: Verify Account and Password
* **End Point:**  `api/v1/user/signin`
* **Method:** `POST`
* **Request Headers:** 

| Field | Type | Description |
| :---: | :---: | :--- |
| Content-Type | String | Only accept `application/json`. |

* **Request Body: JSON Payload**

| Field | Type | Description |
| :---: | :---: | :--- |
| username | String | Required. 3~32 characters. |
| password | String | Required. 8~32 characters.  containing at least 1 uppercase letter, 1 lowercase letter, and 1 number

* **Success Response: 200 (JSON Payload)**

| Field | Type | Description |
| :---: | :---: | :--- |
| success | Boolean | Return True. The validity of the password provided for the given username. |
| reason | String | Return a empty string. Indicating the fail login reason if needed. |

* **Client Error Response: 400 (JSON Payload)**

| Field | Type | Description |
| :---: | :---: | :--- |
| success | Boolean | Return False. The validity of the password provided for the given username. |
| reason | String | Indicating the fail login reason if needed. |

* **To Many Requests: 429 (JSON Payload)**

| Field | Type | Description |
| :---: | :---: | :--- |
| success | Boolean | Return False. The validity of the password provided for the given username. |
| reason | String | Indicating the fail login reason if needed. |

* **Server Error Response: 500 (JSON Payload)**

| Field | Type | Description |
| :---: | :---: | :--- |
| success | Boolean | Return False. The validity of the password provided for the given username. |
| reason | String | Indicating the fail login reason if needed. |
