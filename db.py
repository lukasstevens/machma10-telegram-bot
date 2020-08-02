import sqlite3

from pathlib import Path

class BotDB:

    def __init__(self, db_path_str):
        self.path = Path(db_path_str)
        self.conn = sqlite3.connect(path)
        cursor = self.conn.cursor()

        if not self.db_path.exists():
            sql = open('init.sql', 'r').read()
            cursor.executescript(sql)
            self.conn.commit()


    def __del__(self):
        self.conn.close()

    def get_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id=?', user_id)
        user_tuple = cursor.fetchone()
        if user_tuple is None:
            return None
        else:
            user = {}
            user['id'], user['user_name'], user['first_name'], user['last_name'] = user_tuple
            return user

    def has_user(self, user_id):
        return self.get_user(user_id) is not None

    def get_max_reps(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT exercise_name, MAX(reps) FROM user_reps GROUP BY exercise_name')
        return {exercise: max_reps for (exercise, reps) in cursor.fetchall()}

    def get_max_reps_for_exercise(self, exercise):
        return self.get_max_reps()[exercise]

    def get_user_reps(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT exercise_name, COALESCE(reps, 0) as reps_coalesced FROM exercises RIGHT OUTER JOIN user_reps ON (exercises.exercise_name = user_reps.exercise_name) WHERE user_id=?', user_id)
        return {exercise: reps for (exercise, reps) in cursor.fetchall()}

    def get_user_reps_for_exercise(self, user_id, exercise):
        return self.get_user_reps(user_id)[exercise]

    def get_user_todo_reps(self, user_id):
        max_reps = self.get_max_reps()
        user_reps = self.get_user_reps()
        return {exercise: max_reps - user_reps for exercise in max_reps}

    def add_to_user_reps(self, user_id, exercise, reps):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO user_reps (user_id, exercise_name, reps) VALUES (?, ?, ?)
            ON DUPLICATE KEY UPDATE user_id=user_id, exercise_name=exercise_name, reps=reps+?
            """, (user_id, exercise, reps, reps))
        self.conn.commit()

    def get_exercise_by_alias(self, alias):
        cursor = self.conn.cursor()
        cursor.execute('SELECT exercise_name FROM exercise_aliases WHERE exercise_alias=?', alias)
        return cursor.fetchone()

    def has_alias(self, alias):
        return self.get_exercise_by_alias(alias) is not None

    def has_exercise(self, alias):
        return self.has_alias()

    def add_exercise(self, exercise, link=None):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO exercises (exercise_name, exercise_link) VALUES (?, ?)', (exercise, link))
        cursor.execute('INSERT INTO exercise_aliases (exercise_alias, exercise_name) VALUES (?, ?)', (exercise, exercise))
        self.conn.commit()

    def add_alias(self, exercise, alias):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO exercise_aliases (exercise_alias, exercise_name) VALUES (?, ?)', (alias, exercise))
        self.conn.commit()

    def set_exercise_link(self, exercise, link):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE exercises SET exercise_link=? WHERE exercise_name=?', (link, exercise))
        self.conn.commit()

    def add_user(self, user_id, user_name, first_name, last_name):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO users (user_id, user_name, first_name, last_name) VALUES (?, ?, ?, ?)', (user_id, user_name, first_name, last_name))
        self.conn.commit()








