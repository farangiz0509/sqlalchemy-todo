import hashlib
from sqlalchemy import (
    insert, select, update, delete
)
from database import engine
from tables import tasks_tabe, users_table, genre_table, movie_table, genre_movie_table


def make_password(password: str):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

def create_user(username: str, password: str):
    hashed_password = make_password(password)
    stmt = insert(users_table).values(username=username, hashed_password=hashed_password)
    with engine.connect() as connection:
        connection.execute(stmt)
        connection.commit()

def check_user(username: str, password: str):
    hashed_password = make_password(password)
    stmt = (
        select(users_table)
        .where(
            users_table.columns.username==username, 
            users_table.columns.hashed_password==hashed_password
        )
    )
    with engine.connect() as connection:
        return connection.execute(stmt).first()

def create_task(title: str, description: str | None = None):
    stmt = insert(tasks_tabe).values(title=title, description=description, completed=False)
    with engine.connect() as connection:
        result = connection.execute(stmt)
        connection.commit()
        return result.inserted_primary_key[0]

def get_tasks():
    stmt = select(tasks_tabe).order_by(tasks_tabe.columns.id.asc())
    with engine.connect() as connection:
        tasks = connection.execute(stmt)
        return list(tasks)

def get_one_task(user_id: int, pk: int):
    stmt = select(tasks_tabe).where(tasks_tabe.columns.id==pk, tasks_tabe.columns.user_id==user_id)
    with engine.connect() as connection:
        existing_task = connection.execute(stmt).first()
        if existing_task is None:
            raise Exception('task not found.')
        return existing_task

def update_task(pk: int, title: str | None = None, description: str | None = None):
    if title is None and description is None:
        return
    stmt = select(tasks_tabe).where(tasks_tabe.columns.id == pk)
    with engine.connect() as connection:
        existing_task = connection.execute(stmt).first()
        if existing_task is None:
            raise Exception('Task not found.')
    values = {}
    if title is not None:
        values['title'] = title
    if description is not None:
        values['description'] = description
    stmt = update(tasks_tabe).values(**values).where(tasks_tabe.columns.id == pk)
    with engine.connect() as connection:
        connection.execute(stmt)
        connection.commit()

def delete_task(pk: int):
    stmt = select(tasks_tabe).where(tasks_tabe.columns.id == pk)
    with engine.connect() as connection:
        existing_task = connection.execute(stmt).first()
        if existing_task is None:
            return 'Task not found.'
    stmt = delete(tasks_tabe).where(tasks_tabe.columns.id == pk)
    with engine.connect() as connection:
        connection.execute(stmt)
        connection.commit()
        return 'Task deleted.'

def change_task_status(pk: int):
    stmt = select(tasks_tabe).where(tasks_tabe.columns.id == pk)
    with engine.connect() as connection:
        task = connection.execute(stmt).first()
        if task is None:
            raise Exception('Task not found.')
        current_status = task['completed']
    new_status = not current_status
    stmt = update(tasks_tabe).values(completed=new_status).where(tasks_tabe.columns.id == pk)
    with engine.connect() as connection:
        connection.execute(stmt)
        connection.commit()
    stmt = select(tasks_tabe).where(tasks_tabe.columns.id == pk)
    with engine.connect() as connection:
        updated_task = connection.execute(stmt).first()
        return updated_task

def mark_as_complated(user_id: int, pk: int):
    stmt = update(tasks_tabe).values(complated=True).where(tasks_tabe.columns.id==pk, tasks_tabe.columns.user_id==user_id)
    with engine.connect() as connection:
        connection.execute(stmt)
        connection.commit()

def mark_as_incomplated(user_id: int, pk: int):
    stmt = update(tasks_tabe).values(complated=False).where(tasks_tabe.columns.id==pk, tasks_tabe.columns.user_id==user_id)
    with engine.connect() as connection:
        connection.execute(stmt)
        connection.commit()

def get_movie_by_genre(genre: str):
    stmt = select(genre_table).where(genre_table.columns.name==genre)
    with engine.connect() as conn:
        genre = conn.execute(stmt).first()

    if not genre:
        return []
    
    genre_id = genre[0]
    
    stmt = select(genre_movie_table).where(genre_movie_table.columns.genre_id==genre_id)
    with engine.connect() as conn:
        genre_movies = conn.execute(stmt)

    movies = []
    for genre_movie in genre_movies:
        stmt = select(movie_table).where(movie_table.columns.id==genre_movie[2])
        with engine.connect() as conn:
            movies.append(list(conn.execute(stmt)))

    return movies
