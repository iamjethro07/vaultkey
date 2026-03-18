import os
import pymysql
from flask import g

_cfg = {}

def init_db(app):
    global _cfg
    _cfg = {
        'host':        os.getenv('DB_HOST', '127.0.0.1'),
        'port':        int(os.getenv('DB_PORT', 3306)),
        'user':        os.getenv('DB_USER', 'root'),
        'password':    os.getenv('DB_PASSWORD', ''),
        'database':    os.getenv('DB_NAME', 'vaultkey'),
        'charset':     'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
    }
    @app.teardown_appcontext
    def close(e):
        db = g.pop('db', None)
        if db: db.close()

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(**_cfg)
    return g.db

def query(sql, args=(), one=False, commit=False):
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute(sql, args)
            if commit:
                db.commit()
                return cur.lastrowid
            return cur.fetchone() if one else cur.fetchall()
    except Exception as e:
        if commit: db.rollback()
        raise e

