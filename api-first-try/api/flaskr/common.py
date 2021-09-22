from flask import (
    g
)

from werkzeug.exceptions import abort

from flaskr.db import get_db

def get_post(post_id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (post_id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)  # 403 means “Forbidden”

    return post


def update_post(post_id, data):
    post = get_post(post_id)
    title = data.get('title')
    body = data.get('body')

    db = get_db()
    db.execute(
        'UPDATE post SET title = ?, body = ?'
        ' WHERE id = ?',
        (title, body, post_id)
    )
    db.commit()


def delete_post(post_id):
    get_post(post_id)

    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (post_id,))
    db.commit()