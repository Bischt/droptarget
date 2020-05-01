droptarget
==========

Description:
------------
App to run pinball tournaments.

Design Requirements:
--------------------
1. Responsive Design ("mobile first")
2. Based on Playfield API for backend data access
3. Flask/Python3 (PEP-8 and Black formatting)

Permissioning Roles:
--------------------
1. Player - find, view, register, (queue, scores) tournament specific setting
2. Score Keeper - enter scores for any match/player (Maybe toggle game status?)
3. Tournament Director/TD/Admin - admin functions, and also scorekeeper functions

Navigation Wireframe:
---------------------
**Top Navigation:**
* Context Sensitive? (Link current outstanding action like enter match scores)
* Home
* Find
* Register
* Queue (Setting allowing self joining queues)
* Scoring (Setting allowing self scoring)
* Standings
* Projector icon (Changes to projector friendly view on far right) /dashboard

**User Panels**
_Side Nav1:_
* Matches (For active tournament?)

*Score Keeper Panels:*

_Side Nav1 (Score keeping functions):_
* Enter scores for match/player

*Admin Panels:*

_Side Nav1 (Manage Content):_
* Machines
* Locations
* Players

_Side Nav2 (Meat and Potatos):_
* Manage Tournaments
* Manage Series
* Manage Matches? (To do overrides and fix problems)


Run Locally:
------------
1.  cd to flask directory
2.  `export FLASK_APP=run.py`
    `export FLASK_ENV=development`
3.  Run the app: `flask run`
4.  In browser go to: `http://127.0.0.1:5000/`

Run via Docker:
--------------
1.  In directory with docker-compose.yml: `docker-compose build`
2.  Create & start containers: `docker-compose up`
3.  In browser go to: `http://127.0.0.1`

Shortcut: `docker-compose up --build`