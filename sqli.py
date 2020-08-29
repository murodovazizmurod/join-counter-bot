import sqlite3

class Sql:
    def __init__(self, filename):
        self.con = sqlite3.connect(filename, check_same_thread=False)
        self.cur = self.con.cursor()

    def create(self, group_id):
        with self.con:
            try:
                self.cur.execute(f"""CREATE TABLE [{group_id}] (
                                                                id          INTEGER       PRIMARY KEY AUTOINCREMENT,
                                                                user_id     VARCHAR (50),
                                                                first       VARCHAR (255),
                                                                last        VARCHAR (255),
                                                                added_count INTEGER (11)  DEFAULT (0) 
                                                            );""")
                return True
            except sqlite3.OperationalError:
                return False
    
    def check_user(self, group_id, id):
        with self.con:
            return bool(len(self.cur.execute(f"SELECT * FROM `{group_id}` WHERE `user_id` = ?", (id,)).fetchall()))


    def add(self, group_id, user_id, first, last):
        with self.con:

            self.cur.execute(f"INSERT INTO [{group_id}] (user_id, first, last) VALUES (?,?,?)", (user_id, first, last))
            self.con.commit()

    def give_message(self, group_id, id, count):
        with self.con:
            self.cur.execute(f"UPDATE `{group_id}` SET `added_count` = `added_count` + {count} WHERE `user_id` = ?", (id,))
            self.con.commit()
    
    def results(self, group_id):
        with self.con:
            text = ""
            users = self.cur.execute(f"SELECT * FROM `{group_id}` ORDER BY `added_count` DESC").fetchall()
            for user in users:
                text += f"{user[2]} - {user[4]}\n"
            return text