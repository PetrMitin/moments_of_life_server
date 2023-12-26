Django server for moments_of_life app. Frontend app: https://github.com/PetrMitin/moments_of_life_client.git
To run dev server, install dependencies from requirements.txt, configure and fill postgres database (fill_db [num_users:int]) and run 'python manage.py runserver'.
To run prod server, build frontend app in corresponding directory and run 'gunicorn momentsoflife_server.wsgi:application'.