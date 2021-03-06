import sqlite3


class User():
    def __init__(self, name, password):
        self.name = name
        self.password = password
        email = ""

    def get_name(self):
        return self.name

    def get_pass(self):
        return self.password

    def register(self):
        conn = sqlite3.connect('DB_Users.db')
        c = conn.cursor()
        c.execute('''INSERT INTO users (username, password) VALUES ('{0}', '{1}')'''.format(self.name, self.password))
        conn.commit()
        conn.close()

    def add_email(self, email):
        conn = sqlite3.connect('DB_Users.db')
        c = conn.cursor()
        c.execute('''UPDATE users SET email = '{0}' WHERE username = '{1}' '''.format(email, self.name))
        conn.commit()
        conn.close()
        self.email = email

    def checkname(self):
        conn = sqlite3.connect('DB_Users.db')
        c = conn.cursor()
        usernamelist = list((c.execute("SELECT username from users")))
        if self.name not in (username[0] for username in usernamelist):
            namebool = False
        else:
            namebool = True
        conn.close()
        return namebool

    def checkpass(self):
        conn = sqlite3.connect('DB_Users.db')
        c = conn.cursor()
        passbool = False
        passlist = list((c.execute("SELECT password from users")))
        if self.password not in (passname[0] for passname in passlist):
            pass
        else:
            passbool = True
        conn.close()
        return passbool

    def return_user(self):
        conn = sqlite3.connect('DB_Users.db')
        c = conn.cursor()
        username = c.execute('''SELECT username FROM users WHERE username = '{0}' '''.format(self.name))
        name = username.fetchone()
        conn.close()
        return name[0]
