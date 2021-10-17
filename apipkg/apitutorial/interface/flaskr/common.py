import os
import sqlite3

from apitutorial.database import get_db


def get_users():
    db = get_db()

    posts = db.execute(
        'SELECT username'
        ' FROM user'
        ' ORDER BY username'
    ).fetchall()

    return posts


def get_posts():
    db = get_db()

    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print('*'*79)
    for i in cursor.fetchall():
        print(i['name'])
    print('*'*79)

    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return posts


def get_post(id):
    db = get_db()

    post = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    return post


def delete_post(post_id):
    db = get_db()
    print(db)

