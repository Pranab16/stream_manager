# stream_manager

Used tweepy package to fetch tweets in real-time.

Used swampdragon to show data on UI in real-time.

Steps to run this application:

1. create a new virtualenv

2. Install packages

    ``` pip install -r requirements.txt ```

3. Create a database named 'stream_manager' in postgres.

4. Run migrations

    ``` python manage.py migrate ```

5. Install redis and start the server

6. Run swamp-dragon server

    ``` python manage.py runsd ```

7. Open a new tab and run django server

    ``` python manage.py runserver ```

8. Open browser and hit
    ``` http://localhost:8000 ```
    
This will show tweets count having word 'programming'.
