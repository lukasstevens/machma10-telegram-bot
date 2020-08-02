CREATE TABLE exercises (
    exercise_name TEXT PRIMARY KEY NOT NULL, exercise_link TEXT
);

CREATE TABLE exercise_aliases (
    exercise_alias TEXT PRIMARY KEY NOT NULL,
    exercise_name,
    FOREIGN KEY (exercise_name) REFERENCES exercises(exercise_name)
);

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY NOT NULL,
    user_name TEXT NOT NULL,
    first_name TEXT NOT NULL, 
    last_name TEXT NOT NULL
);

CREATE TABLE user_reps (
    user_id NOT NULL,
    exercise_name NOT NULL,
    reps INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (exercise_name) REFERENCES exercises(exercise_name),
    PRIMARY KEY (user_id, exercise_name)
);
