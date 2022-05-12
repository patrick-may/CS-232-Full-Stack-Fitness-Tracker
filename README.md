# Project: CRUD Lifter

## Description
This is a gym tracking and management software. It currently supports tracking various powerlifting workouts from the perspective of the user.

It lets one add workouts to their profile, update prior misinformation, and delete workouts if needed. Workouts are a collection of weight sets, along with some overall information about the workout. Individual weight sets are able to be edited as desired within the workout.

run `python bootstrap.py` and update `.env` to appropriate local mysql environment variables
then run: `flask initdb` to format your database to our application and clear it
finally:  `flask run`

Then wherever your flask webview is hosted (typically localhost:8000, but this depends on enviroment variables)

First, login as "admin" to Read, Create, Update, Delete gym_members in your organization. After creating at least one gym member that is displayed on the admin page, you may "logout"

Then, login again, using the created member's gym_id that was visible in the admin page. This will take you to the standard user page, where weight set creation, update, delete, and reading are available. 
Workouts are able to be inputted and deleted from this page as well.

When using, make sure to login with either "admin" or a gym_id that you know exists in the database! Otherwise errors will likely occur. Feel free to reach out with any questions or improvement ideas. 

Thank you for taking the time to look at our project. -Patrick & Angad
## API Documentation
API is a work in progress.

The API currently supports:
    CRUD of gym_members
    CRUD of weight_sets
    CR D of workouts

For somewhat better reference, look into `app/api/lifter_api.py` docstrings
