CREATE TABLE exercises (
    exercise_name TEXT PRIMARY KEY, exercise_link TEXT
)

CREATE TABLE exercise_aliases (
    exercise_alias TEXT PRIMARY KEY,
    exercise_name,
    FOREIGN_KEY (exercise_name) REFERENCES exercises(exercise_name)
)

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    user_name TEXT NOT NULL,
    first_name TEXT NOT NULL, 
    last_name TEXT NOT NULL
)

CREATE TABLE user_reps (
    user_id,
    exercise_name,
    reps INTEGER NOT NULL,
    PRIMARY KEY (user_id, exercise_name),
    FOREIGN_KEY (user_id) REFERENCES users(user_id),
    FOREIGN_KEY (exercise_name) REFERENCES exercises(exercise_name)
)
