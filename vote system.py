import os
import mysql.connector
#estabilish database connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="vote_system"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS political_party(party_id varchar(5), party_name varchar(255), party_leader varchar(100), number_of_members int , primary key(party_id));")
mycursor.execute("CREATE TABLE IF NOT EXISTS states(state_id int(3), state_name varchar(100), primary key(state_id));")
mycursor.execute("CREATE TABLE IF NOT EXISTS citizen(citizen_nic varchar(10), citizen_name varchar(255), citizen_age int(3), state_id int, has_voted int default 0, foreign key(state_id) references states(state_id),primary key(citizen_nic)); ")
mycursor.execute("CREATE TABLE IF NOT EXISTS candidate(candidate_id int, candidate_name varchar(255), candidate_nic varchar(255), candidate_age int, candidate_education varchar(255), votes int default 0, primary key(candidate_id), state_id int, foreign key(state_id) references states(state_id),party_id varchar(100), foreign key(party_id) references political_party(party_id));")

class State:
    def __init__(self):
        self.state_id = ''
        self.state_name = ''
        
class Citizen(State):
    def __init__(self):
        self.name = ''
        self.NIC = ''
        self.age = 0
        self.has_Voted = False

      
class PoliticalParty:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.leader = ''
        self.number_of_members = 0
  

class Candidate(Citizen,State):
    def __init__(self):
        super(Candidate, self).__init__();
        self.political_party = ''
        self.votes = 0
        self.candidate_id = ''
        self.education = ''
    
    def add_votes(self):
        self.votes += 1
        

##FUNCTIONS WE NEED##############################################################
#get political party
def get_party():
    mycursor.execute("select party_id,party_name from political_party;")
    myresult = mycursor.fetchall()
    for x in myresult:
        print('     '+x[0]+"."+x[1])
    political_party = input("Select political party[by number]: ")
    return political_party
    
#get state from user
def get_state():
    mycursor.execute("select state_id,state_name from states;")
    myresult=mycursor.fetchall()
    for x in myresult:
        print('     '+str(x[0])+"."+x[1])
    state = input("Select state[by number]: ")
    return state
###############################################################################

def add_candidate():
   
    #get candidate's details from user
    candidate = Candidate()
    candidate.candidate_id = input("Enter Candidate ID : ")
    candidate.name = input("Enter candidate's name: ")
    candidate.NIC = input("Enter candidate's NIC: ")
    candidate.age = int(input("Enter candidate's age: "))
    candidate.education = input("Enter candidate's education: ")
    candidate.political_party=get_party()
    candidate.state_id = get_state()
    
    
    #save candidate details to database
    sql = "INSERT INTO candidate (candidate_id, candidate_name, candidate_nic, candidate_age, candidate_education, state_id,party_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (candidate.candidate_id,candidate.name,candidate.NIC, candidate.age, candidate.education, candidate.state_id,candidate.political_party)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    to_exit = input("Hit Enter to exit...")
    os.system('cls')


    
def add_citizen():
    #get inputs from users
    citizen = Citizen()
    
    citizen.NIC = input("Enter your NIC : ")
    citizen.name = input("Enter Name : ")
    citizen.age = int(input("Enter your age : "))
    citizen.state_id = get_state()
    
    sql = "INSERT INTO citizen(citizen_nic, citizen_name, citizen_age, state_id) VALUES (%s, %s, %s, %s)"
    val = (citizen.NIC, citizen.name, citizen.age, citizen.state_id)
    mycursor.execute(sql, val)
    mydb.commit()
    print("\n")
    print(mycursor.rowcount, "record inserted.")
    to_exit = input("Hit Enter to exit...")
    os.system('cls')
    
def vote():
    #has voted or not
    def has_vote(nic):
        sql = "UPDATE citizen SET has_voted = 1 WHERE citizen_nic = %s"
        val = (nic,)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected") 
        
    #print candidates List to user
    def get_candidate_list():
        mycursor.execute("select candidate_id, candidate_name from candidate;")
        myresult = mycursor.fetchall()
        for x in myresult:
            print('     '+str(x[0])+" - "+str(x[1]))
    citizen_nic = input("Enter your NIC : ")
    
    for i in range(3):
        get_candidate_list()
        count = str(i+1)
        preferense = input("Enter Preference {$count} : ")
        #get vote count belong to that candidate
        sql = "SELECT votes FROM candidate where candidate_id = %s;"
        val = (preferense,)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        for x in result:
            str_result = x[0];
        vote_count = int(str_result)+1#add votes
        #save new votes to database
        sql = "UPDATE candidate SET votes = %s where candidate_id = %s"
        val = (vote_count,preferense)
        mycursor.execute(sql, val)
        mydb.commit()
        print("\n")
        print(mycursor.rowcount, "record inserted.")
        os.system('cls')
    has_vote(citizen_nic)
    to_exit = input("Hit Enter to exit...")
    os.system('cls')

def add_politicalParty():
    #get inputs from user
    party = PoliticalParty()
    
    party.id = input("Enter ID of the party : ")
    party.name = input("Enter Name of the party : ")
    party.leader = input("Enter party leader name : ")
    party.number_of_members = int(input("Enter Number of members : "))
    
    #save input to database
    sql = "INSERT INTO political_party (party_id, party_name, party_leader, number_of_members) VALUES (%s, %s, %s, %s)"
    val = (party.id, party.name, party.leader, party.number_of_members)
    mycursor.execute(sql, val)
    mydb.commit()
    print("\n")
    print(mycursor.rowcount, "record inserted.")
    to_exit = input("Hit Enter to exit...")
    os.system('cls')
    
def add_state():
    #get inputs from user 
    state = State()
    state.state_id = int(input("Enter Province ID : "))
    state.state_name = input("Enter province name : ")
    sql = "INSERT INTO states (state_id, state_name) VALUES (%s, %s)"
    val = (state.state_id, state.state_name)
    mycursor.execute(sql, val)
    mydb.commit()
    print("\n")
    print(mycursor.rowcount, "record inserted.")
    to_exit = input("Hit Enter to exit...")
    os.system('cls')

def main_menu():
    print('     1.Add Citizen') 
    print('     2.Add Candidate')
    print('     3.Add Political Party')
    print('     4.Add State')
    print('     5.Vote')
    print('     6.exit')
        
    choise = int(input("What do you want to do ? "))
    return choise

while(True):
    choise = main_menu()
    if choise == 1:
        add_citizen()
    elif choise == 2:
        add_candidate()
    elif choise == 3:
        add_politicalParty()
    elif choise == 4:
        add_state()
    elif choise == 5:
        vote()
    elif choise == 6:
        os.system('cls')
        break
    else:
        print("Invalid choise")
    