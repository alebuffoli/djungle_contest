# Djungle Contest


## Acknowledge

The application uses a random method to indicate the winnings.
1. The code of this applications supposes that the requests that come per day are `prize_per_day` cubed. But In any case, if we want to change the number of request that come per day, we can! Simply edit the number returned from the function `n_requests_estimate` in `/api/utilities.py`. The program will autocalculate the probability for each win.
2. Due to the fact that the application uses a random method to extract the winner, sometime the contest ends with > 95% of prizes given, leaving a 5% of prizes not given away. 
So, to solve this problem and be (almost) sure to give away all the prizes, if the requests that came to the day are greater than 90% and all the prizes are still not already given away, the code implements a boost to increase the probability to win. 

______

## Installation and Start

Run the following commands
1. `python -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python manage.py migrate`
5. `python manage.py populate_db`
   This command creates 4 contest and 3 users.
###
   - The users "user1", "user2", have the password "testing321"
   - The ID of the user1 is `1`, user2 is `2`
   - the user admin has the password "admin"
###

   - C0001 Is a standard contest with no need to login to partecipate.
   - C0002 Is a standard contest that is expired.
   - C0003 Is a contest that needs an authorization to partecipate (the "user1" has the authorization to partecipate, the "user2" no).
   - C0004 Is a contest that needs an authorization to partecipate and each user can win just 2 times per day. (the "user1" has the authorization to partecipate, the "user2" no).

6. `python manage.py runserver` Runs the application


###

- If you want to create a new user, you can use the django admin interface here: http://127.0.0.1:8000/admin/ (Username admin, Password admin)

- If you want to give a user the permission to partecipate to a contest, go here: http://127.0.0.1:8000/admin/api/usertocontest/ and create the association.

_____


## How To
To partecipate to the contest make an api call to the following endpoint:

`/play/?contest={code}`

You can call the endpoint with the method GET.

*The parameter `contest` is strictly required.*

*There is also another parameter `user_id` that allows the user to participate to special contests (Needs the user to be Authorized and Authenticate)*

To partecipate to the contest that require authentication, login with the following endpoint and use the `access` token to partecipate.

`/api/token/`



_____

## Simulate

If you want to simulate a "real life example" you can run the following command.

It will run a series of contests and logs the result in the terminal.


```
pytest -s api/tests/integration_test/test_play_endpoint.py -k 'test_real_contest' --wins_per_day 10 --contests 10
```
*Be aware that the higher the `wins_per_day` are, the longer it will take to conclude the simulation.*

**Commands Info:**

`wins_per_day` specify the number of prizes that can be won per day.

`contests` specify the number of contests that needs to be run.

_____

## Testing purposes

Run `pytest` to test all the tests.


