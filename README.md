Django server for moments_of_life app. Frontend app: https://github.com/PetrMitin/moments_of_life_client.git
To run dev server, install dependencies from requirements.txt, configure and fill postgres database (fill_db [num_users:int]) and run 'python manage.py runserver'.
You can use ready-to-go database dump from db_dump.sql or use fill_db command, but in the last case you also should change user_id and curr_user_id in views to the one generated in your database.
This is for testing purposes only, when authorization is implemented the hardcoded values will be gone.