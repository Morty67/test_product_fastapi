# FastAPI for a simple Product Management System
This project is the server-side component of a web application that provides an API for managing a simple Product Management System

## Technologies Used

*  Backend: FastAPI.
*  Database: SQlite.


## Installing / Getting started:
```shell
To get started, you need to clone the repository from GitHub: https://github.com/Morty67/test_product_fastapi
Python 3.11.3 must be installed

python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)

pip install -r requirements.txt

alembic upgrade head
uvicorn app.main:app --reload

```

## How to get access
Domain:
*  localhost:8000 or 127.0.0.1:8000

## Features:
*  Product Creation: Create new products by providing their name, description, and price.
*  Product Retrieval: Retrieve information about a product using its unique identifier.
*  Product Update: Modify the name, description, or price of a product based on its unique identifier.
*  Product Deletion: Delete a product from the database using its unique identifier.
*  Documentation is located at doc/
