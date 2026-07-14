CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                           username TEXT NOT NULL UNIQUE,
                                                                  hash TEXT NOT NULL);


CREATE TABLE habits (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            user_id INTEGER NOT NULL,
                                                            name TEXT NOT NULL,
                                                                      streak INTEGER NOT NULL DEFAULT 0,
                                                                                                      last_checkin_date TEXT,
                     FOREIGN KEY (user_id) REFERENCES users(id));


CREATE TABLE checkins (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                              habit_id INTEGER NOT NULL, date TEXT NOT NULL,
                                                                                   completed INTEGER NOT NULL DEFAULT 1,
                       FOREIGN KEY (habit_id) REFERENCES habits(id));
