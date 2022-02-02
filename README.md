# Djungle Contest


## Acknowledge

The application uses a random method to indicate the winnings.
1. The code of this applications supposes that the requests that come per day are `prize_per_day` cubed.
2. Due to the fact that the application uses a random method to extract the winner, sometime the contest ends with > 95% of prizes given, leaving a 5% of prizes not given away. 
So, to solve this problem and be (almost) sure to give away all the prizes, if the requests that came to the day are greater than 90% and all the prizes are still not already given away, the code implements a boost to increase the probability to win. 

______

## Installation and Start

Run the following commands
1. `python -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python manage.py migrate`

5. `python manage.py create_contest`
   (This command creates 2 contest (C0001 & C0002) with 45 prize per day each. The contest `C0001` is valid, instead the `C0002` is expired.)

6. `python manage.py runserver` Runs the application


_____

## Simulate

If you want to simulate a "real life example" you can run the following command.

It will run a series of contests and logs the result in the terminal.


```
pytest -s api/tests/integration_test/test_play_endpoint.py -k 'test_real_contest' --wins_per_day 20 --contests 10
```
*Be aware that the higher the `wins_per_day` are, the longer it will take to conclude the simulation.*

**Commands Info:**

`wins_per_day` specify the number of prizes that can be won per day.

`contests` specify the number of contests that needs to be run.

_____

## Testing purposes

Run `pytest` to test all the tests.

_____


## How To
There is just the following endpoint in this application:

`/play/?contest={code}`

You can call the endpoint with the method GET.

*The parameter `contest` is strictly required.*

