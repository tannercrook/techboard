# /models/User.py


from techBoard.models.DBase import connection
import hashlib, uuid
import sys


class User:

    def __init__(self):
        self.userID = 0
        self.user_id = 0
        self.username = "NOT SET"
        self.email = "NOT SET"
        self.lastName = "NOT SET"
        self.firstName = "NOT SET"
        self.password = "NOT SET"
        self.salt = ""
        self.is_authenticated=False
        self.is_active=False
        self.is_anonymous=False 
        self.user_id=0

    def getEmail(self):
        return self.email

    def getPassword(self):
        return self.password

    def get_id(self):
        return self.user_id

    def setCreds(self, email, username, password):
        self.email = email
        self.password = password 
        self.username = username

    def makeUserFromCreds(self):
        try:
            c, conn = connection()
            c.execute("SELECT system_user_id, email, username, password, salt FROM techboard.system_user WHERE username='{}';".format(str(self.username)))
            result_set = c.fetchall()
            conn.close()

            # Check the results
            if(len(result_set) == 1):
                for row in result_set:
                    self.userID = row['system_user_id']
                    self.username = row['username']
                    self.email = row['email']
                    self.user_id = chr(row['system_user_id'])
                    realPassword = row['password']
                    self.salt = row['salt']
                    hashedPassword = hashlib.sha512(self.password+self.salt.encode('utf-8')).hexdigest()
                    if hashedPassword == realPassword:
                        self.is_authenticated = True
                        self.is_anonymous = True
                        self.is_active = True
                        return True
                    else:
                        return False
            else:
                # Something isn't right
                return False

        except Exception as e:
            return str(e)

    def get(self, user_id):
        try:
            c, conn = connection()
            c.execute("SELECT system_user_id, email, username, password FROM techboard.system_user WHERE system_user_id={};".format(int(ord(user_id))))
            result_set = c.fetchall()
            conn.close()

            # Check the results
            if(len(result_set) == 1):
                for row in result_set:
                    self.userID = row['system_user_id']
                    self.email = row['email']
                    self.username = row['username']
                    self.user_id = chr(row['system_user_id'])
                    self.is_authenticated = True
                    self.is_anonymous = True
                    self.is_active = True
                    return self
            else:
                # Something isn't right
                return None

        except Exception as e:
            return(self)

    def createUser(self):
        try:
            c, conn = connection()
            c.execute("INSERT INTO systemuser (email,lastname,firstname,password,salt) VALUES (%s,%s,%s,%s,%s);",(self.email,self.lastName,self.firstName,self.password,self.salt))
            conn.commit()
            conn.close()
            return "<p> Create Successfully </p>"
        except Exception as e:
            return str(e)
