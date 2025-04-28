import sqlite3
import hashlib
import logging
from datetime import datetime, timedelta
from config import DB_PATH

logger = logging.getLogger(__name__)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            file_id TEXT,
            file_name TEXT,
            file_type TEXT,
            uuid TEXT UNIQUE,
            timestamp DATETIME,
            password TEXT,
            is_protected BOOLEAN DEFAULT FALSE
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS password_attempts (
            user_id INTEGER,
            file_uuid TEXT,
            attempts INTEGER DEFAULT 0,
            last_attempt DATETIME,
            PRIMARY KEY (user_id, file_uuid)
        )
    ''')

    conn.commit()
    conn.close()

def add_file(user_id, file_id, file_name, file_type, uuid, timestamp, password=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        is_protected = password is not None
        password_hash = hashlib.sha256(password.encode()).hexdigest() if password else None

        c.execute('''
            INSERT INTO files (user_id, file_id, file_name, file_type, uuid, timestamp, password, is_protected)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, file_id, file_name, file_type, uuid, timestamp, password_hash, is_protected))
        conn.commit()
    except Exception as e:
        logger.error(f"Ошибка добавления файла: {e}")
    finally:
        conn.close()

def update_file_password(uuid_val, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        is_protected = True
        c.execute('''UPDATE files SET password=?, is_protected=? WHERE uuid=?''', (password_hash, is_protected, uuid_val))
        conn.commit()
        logger.info(f"Пароль файла {uuid_val} обновлен")
    except Exception as e:
        logger.error(f"Ошибка обновления пароля файла: {e}")
    finally:
        conn.close()

def delete_file(uuid_val, user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    deleted = False
    try:
        c.execute('DELETE FROM files WHERE uuid=? AND user_id=?', (uuid_val, user_id))
        conn.commit()
        deleted = c.rowcount > 0
        logger.info(f"Удаление файла {uuid_val}: {'Успешно' if deleted else 'Не найдено'}")
    except Exception as e:
        logger.error(f"Ошибка удаления файла: {e}")
    finally:
        conn.close()
    return deleted

def get_file(uuid_val, user_id=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    result = None
    try:
        if user_id:
            c.execute('SELECT * FROM files WHERE uuid=? AND user_id=?', (uuid_val, user_id))
        else:
            c.execute('SELECT * FROM files WHERE uuid=?', (uuid_val,))
        result = c.fetchone()
    except Exception as e:
        logger.error(f"Ошибка получения файла: {e}")
    finally:
        conn.close()
    return result

def get_user_files(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    result = []
    try:
        c.execute('SELECT uuid, file_name, timestamp, is_protected FROM files WHERE user_id=?', (user_id,))
        result = c.fetchall()
        logger.debug(f"Найдено файлов для {user_id}: {len(result)}")
    except Exception as e:
        logger.error(f"Ошибка получения файлов: {e}")
    finally:
        conn.close()
    return result

def increment_password_attempts(user_id, file_uuid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO password_attempts (user_id, file_uuid, attempts, last_attempt)
            VALUES (?, ?, 1, ?)
            ON CONFLICT(user_id, file_uuid) DO UPDATE SET
                attempts = attempts + 1,
                last_attempt = ?
        ''', (user_id, file_uuid, datetime.now(), datetime.now()))
        conn.commit()
    except Exception as e:
        logger.error(f"Ошибка увеличения количества попыток: {e}")
    finally:
        conn.close()

def get_password_attempts(user_id, file_uuid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('''
            SELECT attempts, last_attempt FROM password_attempts
            WHERE user_id=? AND file_uuid=?
        ''', (user_id, file_uuid))
        result = c.fetchone()
        if result:
            attempts, last_attempt_str = result
            last_attempt = datetime.strptime(last_attempt_str, '%Y-%m-%d %H:%M:%S.%f') if isinstance(last_attempt_str, str) else last_attempt_str

            return attempts, last_attempt
        else:
            return 0, None
    except Exception as e:
        logger.error(f"Ошибка получения количества попыток: {e}")
        return 0, None
    finally:
        conn.close()

def reset_password_attempts(user_id, file_uuid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('''
            DELETE FROM password_attempts
            WHERE user_id=? AND file_uuid=?
        ''', (user_id, file_uuid))
        conn.commit()
    except Exception as e:
        logger.error(f"Ошибка сброса количества попыток: {e}")
    finally:
        conn.close()
