## Thought Process

- Created 3 entities i.e User, Team and project board.
- Chose django framework in order avoid writing custom logic for table joins.
- Segregated the entities into django apps which helped in creating separate endpoints and models for each entity.
- Created a common util module to store functions which can be useful to each app.
- Wrote implementation to derived classes which are the inherting the base class.
- endpoints are present in **urls.py** of each app.
- database schema is specified in **models.py** of each app.
- Implementation of the base class is in **views.py** of each app.
- `factwise_project_planner` dir holds the center urls.py

## Execution Steps

1. Run `python -m pip install -r requirements.txt` at the location where requiremenrts.txt is present
2. Run `python manage.py makemigrations` and `python manage.py migrate` to sync models with sqlite Db from location where manage.py is present.
3. Run `python manage.py runserver` from the location of `manage.py` file.
4. Start playing with planner using the curls specified in the postman collection by importing `project_planner.postman_collection.json` into postman.
5. Create entities in the order of **USER -> TEAM -> BOARD**
6. `project_board/export_board` will save the report of board  in `out` directory with current timestamp as prefix.

NOTE : Remove `db/db.sqlite3` file to clear the database

## Assumptions

- **Installed python in the system**.
- Handled common edges cases like boundary checks/ empty check mostly for user model in order to complete faster.
- In order to implement the base cases had to use django rest framework.
- Creatinf apps for user, team and project in order to maintain segreation and easy data connectivity using ORM and models.
- Inside a project board, we can have multiple tasks and each should be identified by the user_id and board_id.
- Keeping all the id fields as auto increments integer field.
- All Creation time  should be handled by application not to be requsted by client.
- Max length for status of project board and tasks as 20
- When creating a task both team_id and user_id are needed.
