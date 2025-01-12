# ALX Final Capstone Project 
Blog Api Application

1. Create a virtual environment.
 ```sh
    python -m venv env
 ```
2. Activate virtual environment.
```sh
    source /path/to/venv/bin/activate`
```
3. Install project dependencies `pip install -r requirements.txt`


4. Start server.
 ```sh
 python manage.py runserver 
```
 you could also specify the host and port to run 
 ```sh
 python manage.py runserver ${host} ${port}
 ```

To visit Live Link 
[Live Link](https://alx-capstone-drab.vercel.app/)

# Endpoints 


1. /api/users/ POST fields : username , email , password , first_name , last_name
2. /api/login/ POST fields : email , password
3. /api/blogs/ POST(AUTHENTICATED) fields : title , content, author , published_date , tags , categories
4. /api/blogs/<int>/ GET This endpoint Gets a blogs by its id
5. /api/blogs/ GET this endpoint gets all blogs
6. /api/blogs/<int>/ PUT(AUTHENTICATED) fields : title , content, author , published_date , tags , categories
7. /api/blogs/<int>/ DELETE(AUTHENTICATED) : Deletes a blog the user must be the owner of the blog unless it returns a 403
8. /api/users/<int>/ GET : Gets a user by id

