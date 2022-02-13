import sqlite3 as sq
import time

class backEnd():
    def __init__(self) -> None:
        self.con = sq.connect("wallets.db")
        self.cur = self.con.cursor()
        try:
            self.cur.execute('CREATE TABLE mywallets \
                (date text, group_name text, contact text, amount int, transaction_type int)')
        except sq.OperationalError:
            pass
    

    def addValue(self, group, contact, amount, type):
        log = time.asctime()
        entry = (log, group, contact, amount, type)
        self.cur.execute(f"INSERT INTO mywallets VALUES (?, ?, ?, ?, ?)", entry)
        self.con.commit()


    def addMultiple(self, mass_entry):
        log = time.asctime()
        self.cur.executemany(f"INSERT INTO mywallets VALUES (?, ?, ?, ?, ?)", mass_entry)
        self.con.commit()


    def readWallet(self, group=None):
        """read data base and return all informations for this wallet page in a dictionnary:
        :contacts as key pointing to a list:
        :money spent at index 0
        :money paid at index 1
        """
        if not group:
            print("no wallet was found")
            return
        
        walletRead = self.cur.execute(
            f"SELECT contact \
            FROM mywallets \
            WHERE group_name = '{group}'"
            )

        contacts = {contact[0]:[0, 0] for contact in walletRead }
        money_spent = self.cur.execute(
            f"SELECT contact, amount \
            FROM mywallets \
            WHERE transaction_type = 'spent'\
            AND group_name = '{group}' \
            GROUP BY contact  "
            )  

        for value in money_spent:
            contacts[value[0]][0] = value[1]

        money_paid = self.cur.execute(
            f"SELECT contact, amount \
            FROM mywallets \
            WHERE transaction_type = 'paid' \
            AND group_name = '{group}' \
            GROUP BY contact "
            )        
        for value in money_paid:
            contacts[value[0]][1] = value[1]   
        print(contacts)
        return contacts
    
    def getGroups(self):
        """return all the group names in a tuple to filter unique values only
        will feed the scrolled widget for dynamic display of ongoing groups"""
        self.groupList = {x for x in self.cur.execute(
            f"SELECT group_name FROM mywallets")
            }
        return self.groupList
    

    def closeCon(self):
        self.con.close()
    
    def getData(self, group=None):
        for value in self.cur.execute(f"SELECT * FROM mywallets WHERE group_name = '{group}'"):
            print(value)



if __name__ == "__main__":
    db = backEnd()
    events = [
        ("12 august 2022", "birthday", "Jess", 45, "spent"), 
        ("12 august 2022", "birthday", "anthony", 70, "spent"), 
        ("01 january 2022","birthday", "anthony", 90, "spent"),
        ("12 august 2022", "travel", "John", 500, "paid"),
        ("12 august 2022", "birthday", "Jess", 20, "paid"), 
    ]

    # db.addMultiple(events)
    #payment archetypes : spent = money invested, payed = money reimboursed to group, create = creation
    db.readWallet("birthday")
    # db.getData("birthday")

