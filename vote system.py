import os
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
#estabilish database connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="vote_system"
)

mycursor = mydb.cursor()

#Create tables
mycursor.execute("CREATE TABLE IF NOT EXISTS political_party(party_id varchar(5), party_name varchar(255), party_leader varchar(100), number_of_members int , primary key(party_id));")
mycursor.execute("CREATE TABLE IF NOT EXISTS states(state_id int(3), state_name varchar(100), primary key(state_id));")
mycursor.execute("CREATE TABLE IF NOT EXISTS citizen(citizen_nic varchar(10), citizen_name varchar(255), citizen_age int(3), state_id int, has_voted int default 0, foreign key(state_id) references states(state_id),primary key(citizen_nic)); ")
mycursor.execute("CREATE TABLE IF NOT EXISTS candidate(candidate_id int, candidate_name varchar(255), candidate_nic varchar(255), candidate_age int, candidate_education varchar(255), votes int default 0, primary key(candidate_id), state_id int, foreign key(state_id) references states(state_id),party_id varchar(100), foreign key(party_id) references political_party(party_id));")

#create classes
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
    
        

##FUNCTIONS WE NEED##############################################################
#get political party
def get_party():
    mycursor.execute("select party_id,party_name from political_party;")
    my_result = mycursor.fetchall()
    for x in my_result:
        print('     '+x[0]+"."+x[1])
    political_party = input("Select political party[by number]: ")
    return political_party
    
#get state from user
def get_state():
    mycursor.execute("select state_id,state_name from states;")
    my_result=mycursor.fetchall()
    for x in my_result:
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
    
    #save citizen details to database
    sql = "INSERT INTO citizen(citizen_nic, citizen_name, citizen_age, state_id) VALUES (%s, %s, %s, %s)"
    val = (citizen.NIC, citizen.name, citizen.age, citizen.state_id)
    mycursor.execute(sql, val)
    mydb.commit()
    print("\n")
    print(mycursor.rowcount, "record inserted.")
    to_exit = input("Hit Enter to exit...")
    os.system('cls')
    
def vote():
    #save the voted citizen to database
    def has_vote(nic):#this function update database after user votes
        sql = "UPDATE citizen SET has_voted = 1 WHERE citizen_nic = %s"
        val = (nic,)
        mycursor.execute(sql, val)
        mydb.commit()
        
    def get_voter_province(nic):#This Function get and return province of voter
        sql = "SELECT state_id FROM citizen where citizen_nic = %s;"
        val = (nic,)
        mycursor.execute(sql ,val)
        my_result = mycursor.fetchall()
        for x in my_result:
            province=x[0]
            return province 
        
    #print candidates List to user
    def get_candidate_list(province): #This function get candidate list belong to voter's province
        sql = "SELECT candidate_id, candidate_name from candidate WHERE state_id=%s;"
        val = (province,)
        mycursor.execute(sql, val)
        my_result = mycursor.fetchall()
        for x in my_result:
            print('     '+str(x[0])+" - "+str(x[1]))
    
    def check_age(nic):#this function check whether paticular person old enough to vote or not
        sql ="SELECT citizen_age FROM citizen where citizen_nic = %s;"
        val = (nic,)
        mycursor.execute(sql, val)
        my_result = mycursor.fetchall()
        age =0
        for x in my_result:
            age = x[0]
        if age>18:
            return True
        
    def voted(nic): #this function check whether citizen voted or not
        sql = "SELECT has_voted FROM citizen where citizen_nic = %s;"
        val = (nic,)
        mycursor.execute(sql, val)
        my_result = mycursor.fetchall()
        for x in my_result:
            if x[0]==0:
                return True
            else:
                return False
    
    def if_citizen(nic):#This function check if a paticular person citizen or not
        mycursor.execute("SELECT citizen_nic FROM citizen;")
        my_result = mycursor.fetchall()
        for x in my_result:
            if x[0]==nic:
                return True
                break
            else:
                return False
    
    def check_all_conditions(nic):#This function check whether all condition true or not
        age=check_age(nic)
        vote= voted(nic)
        chk_citizen  = if_citizen(nic)
        if chk_citizen == False:
            print("Invalid Citizen ID or Not a valid citizen.")
        if age==False:
                print("You are not old enough to vote!")
        if vote == False:
            print("You voted once!")
        if age == True and vote == True and chk_citizen == True:
            return True
        else:
            return False
       
       
            
    citizen_nic = input("Enter your NIC : ")
    
    all_conditions = check_all_conditions(citizen_nic)
    
    if all_conditions == True:
        province = get_voter_province(citizen_nic)
        for i in range(3):
            get_candidate_list(province)
            count = str(i+1)
            preferense = input("Enter Candidate id to vote : ")
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
            print("\n----------------------------------\n")
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
    
#display result 
def display_result():
    def get_result():#This function get result of all candidates and add their names and result to arrays
        mycursor.execute("SELECT candidate_name, votes FROM candidate")
        my_result = mycursor.fetchall()
        names = []
        votes = []
        for x in my_result:
            names.append(x[0])
            votes.append(x[1])
        return names,votes
    
    name_array,vote_array = get_result()
    
    x = np.array(name_array)
    y = np.array(vote_array)

    plt.bar(x,y)
    plt.show()

        
        

def main_menu():#This function display main menu
    print('     1.Add Citizen') 
    print('     2.Add Candidate')
    print('     3.Add Political Party')
    print('     4.Add State')
    print('     5.Vote')
    print('     6.Display Result')
    print('     7.exit')
        
    choise = int(input("What do you want to do ? "))
    return choise

while(True):
    choise = main_menu()
    if choise == 1:
        how_many = int(input("How many citizen do you want to add ? "))
        for i in range(how_many):
            add_citizen()
    elif choise == 2:
        how_many = int(input("How many candidates do you want to add ? "))
        for i in range(how_many):
            add_candidate()
    elif choise == 3:
        how_many = int(input("How many Political Parties do you want to add ? "))
        for i in range(how_many):
            add_politicalParty()
    elif choise == 4:
        how_many = int(input("How many states do you want to add ? "))
        for i in range(how_many):
            add_state()
    elif choise == 5:
        vote()
    elif choise == 6:
        display_result()
    elif choise == 7:
        os.system('cls')
        break
    else:
        print("Invalid choise")
    