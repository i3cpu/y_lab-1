# FastAPI Restaurant Menu CRUD API

## About

This project is a FastAPI application that provides a RESTful API for managing restaurant menus, submenus, and dishes. It uses PostgreSQL as the database to store the data.



## Getting Started
1. Make sure you have Python and pip (Python package installer) installed.
2. Activate or create a virtual environment (venv) to isolate the project.
  Install the required dependencies listed in the requirements.txt file using the command:

<pre>
```   pip3 install -r requirements.txt
```
</pre>

3. Create the .env file in the project root with your PostgreSQL database connection details:

<pre>
```   DATABASE_URL=postgresql://username:your_password@localhost/your_db
```
</pre>

4. To perform migration, execute the Python file models.py to create tables in the database.
<pre>
```   python3 models.py
```
</pre>

5. Start the FastAPI application using Uvicorn:

<pre>
```   uvicorn main:app --reload
```
</pre>





        




