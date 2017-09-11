# README #

Simple API with Flask, and MongoDB

Based code reference from the article ["Designing a RESTful API with Python and Flask"](https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask)

|Id  | HTTP Method| URI                                        | Action                           |
|----|:-----------:|:------------------------------------------| ---------------------------------|
| 1  |POST       |http://[hostname]/dota2test/api/v0.1/rangking| Given a list of player(s) (either player_id or username and assuming all players have a Dota2 public profile*), return a leaderboard of the players based on their win rate over time (last week, last month, last year and all time)|

*Dota 2 API](https://docs.opendota.com/
