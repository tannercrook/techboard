# /models/Issue.py

# this is the class that defines issues in python from the database.

from techBoard.models.DBase import connection


class Issue:

    def __init__(self):
        self.issueID = 0
        self.title = ""
        self.description = ""
        self.status = ""
        self.instructionBox = 0
        self.instructions = None 
        self.active = 0
        self.createdDate = ""
        self.modifiedDate = ""

    
    def fetch(self):
        try:
            c, conn = connection()
            c.execute("SELECT * FROM issue WHERE issue_id='{}';".format(self.issueID))
            result_set = c.fetchall()
            conn.close()

            # Check the results
            if(len(result_set) == 1):
                for row in result_set:
                    self.title = row["title"]
                    self.description = row["description"]
                    self.status = row["status"]
                    self.instructionBox = row["instruction_box"]
                    self.instructions = row["instructions"]
                    self.active = row["active"]
                    self.createdDate = row["created_date"]
                    self.modifiedDate = row["modified_date"]

                return True
                    
            else:
                # There wasn't a row with that ID
                return False

        except Exception as e:
            return(e)

    def store(self):
        try:
            c, conn = connection()
            preSql = "INSERT INTO techboard.issue (title, description, status, instruction_box, instructions, active) "
            valuesSql = "VALUES(%s,%s,%s,%s,%s,%s);"
            c.execute(preSql+valuesSql,(self.title,self.description,self.status,self.instructionBox,self.instructions,self.active))
            conn.commit()
            conn.close()

            return True

        except Exception as e:
            return(e)

    def update(self):
        try:
            c, conn = connection()
            sql = "UPDATE techboard.issue SET title=%s, description=%s, status=%s, instruction_box=%s, instructions=%s, active=%s WHERE issue_id = %s;"
            c.execute(sql,(self.title,self.description,self.status,self.instructionBox,self.instructions,self.active,self.issueID))
            conn.commit()
            conn.close()

            return True

        except Exception as e:
            return(e)