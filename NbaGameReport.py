# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 21:35:58 2021

@author: Denzel
"""

import requests #imports request module
import pandas as pd #imports pandas 
from datetime import date, timedelta #impoprts datetime module

yesterday = date.today() - timedelta(1) # sets variable for yesterday (today -1)
yes = (yesterday.strftime('20%y%m%d')) #prints yesterday in yyyymmdd format
yes = str(yes) # changes yesterday date that is held under the variable yes to a string

teams = ['76ers', 'Bucks', 'Bulls', 'Cavaliers', 'Celtics', 'Clippers', 'Grizzlies', 'Hawks', 'Heat', 'Hornets', 'Jazz', 'Kings', 'Knicks', 'Lakers', 'Magic', 'Mavericks', 'Nets', 'Nuggets', 'Pacers', 'Pelicans', 'Pistons', 'Raptors', 'Rockets', 'Spurs', 'Suns', 'Thunder', 'Timberwolves', 'Trail Blazers', 'Warriors', 'Wizards']
print("welcome to  NBA game review, here you can select the scores you would like to see for last nights games or games from any date in the season")
print("would you like to see games from last night or from a previous day in the season")
Continue = True #variable created to opperate while loop
while(Continue):
    choi = input("type last night for last nights scores or type season day for the scores of a day in the season")
    if choi == "season day": # this lines sets conditions for the user input if it is equal to season day
        cho = (input("please enter a date in this format yyyymmdd")) 
        if cho.isnumeric(): #if the user input is a number
            cho = int(cho) # changes the user input from a string to an integer 
            if cho >= 20181016 and cho <= int(yes): # checks to see if the date entered by he user is between the date of the start of the season and the dae of last night
                cho = str(cho) # if the date enetered by the user follows the condition above it will be turned back to a string so it is able to be concatnated to other stings
                base_url = "http://www.espn.com/nba/scoreboard/_/date/" # url of website without date( this date automaticaly sets to the current day) set under variable base_url
                final_url = (base_url + cho) # new variable is creating which is equal to the date the user entered added to the base url(url without date)
                url = final_url # new variable created which sets the value of the final_url to the variable url
                r = requests.get(url) # this function packages the request sends the request to the http server and gets the response 
                html_doc=r.text # returns html response to text under the variable htlm_doc
                
                team_names_junk = [] # list is created called team_names_junk
                def find_teams(doc): # function is def (find_teams) with the parameter doc
                    start = doc.find('shortDisplayName') # uses .find method to locate shortDisplayNames on the website source code
                    start = start + 18 # number of characters for short display name
                    end = start + 50 # end of characters for short display name
                    terminate = doc.find('</head>') #stops searching doc at </head> 
                    
                    name = doc[start:end] #applys the start and end to the doc
                    name_list = name.split(',') # splits each string in name turning into a list
                    name = name.replace(" ", "") # gets rid of spaces 
                    team = name_list[0].strip('"') # takes the fist index of name_list and removes "
                    team_names_junk.append(team) # adds team into team_names_junk list
                    if end < terminate:
                        find_teams(doc[end:])
                    else:
                        print("")
                    
                find_teams(html_doc) #call function on HTML doc 
                
                team_list = [] #new list is created under the variable team_list
                for team in team_names_junk: # setting conditions for team_names_junk
                    try: #goes throught with program to make sure teams are in team_names_junk
                        if team in teams: #sets conditions for if team is in the imported list teams from file nba_teams2
                            team_list.append(team) #adds team to list team_list
                            
                    except IndexError: # if there is an index error the program will continue to run 
                        print("")
                    
                team_scores = [] # new list team_scores is created 
                
                def find_team_score(doc): #new funvction is def to catch team scores with the parameter doc
                    start = doc.find('homeAway') # .find method is used to find "homeAway in the html doc 
                    
                    end = start + 40 # sets end of character in html doc to 40 characters 
                    terminate = doc.find('</head>') # doesnt not search head (</head> data is ont used )
                    
                    sc = doc[start:end] #applys start and end to doc and stores the data unnder the variable sc
                    
                    sc_list = sc.split(',')  #splits each string in sc turning into a list
                    sco = sc_list[1] # new variable sco is set to the first index of sc_list
                    scor = sco.split(':') #splits the list at :
                    score = scor[-1].strip('"') 
                    score = int(score)
                    team_scores.append(score)
                    if end < terminate:
                        find_team_score(doc[end:])
                    else:
                        print("")
                    
                    
                find_team_score(html_doc) #calls function on html_doc
                
                for i in team_scores: #sets conditions for objects in list team_scores. Iterates through objects
                    if i == "" or i < 36: # if the object in list equals an empty string or the value is less then 36 the object will be removed from the list
                        team_scores.remove(i) #i is taken out of list
                    elif len(team_list) != len(team_scores): # if then length of team_list is not equal to the length of team_scores (if the asmount of objects in each list do not match)
                        team_scores.pop() # the last object in the list team_scores will be removed
                        
                    
                    
                h_team, a_team, h_score, a_score = [],[],[],[] #list are created under variables h_team, a_team, h_score, a_score
                
                def match_data(teams,scores): # new funnction match_data is created with 2 perameters teams and scores

                    for i in range(0,len(scores),2): #this line iterates through 
                        h_team.append(teams[i]) # next 4 lines matches every other index in a_socre with every other index in a_team and matches every 1st index in h_score with every 1st index in h_team
                        a_team.append(teams[i+1])
                        h_score.append(scores[i])
                        a_score.append(scores[i+1])
                    if len(teams) != len(scores): #if the amount of objects in team does not match the amount of objects in scores the statement below will be printed 
                        print("there is a missmatch somewhere")
                        
                match_data(team_list,team_scores) #calls function match_data
                
                data = {"HOME" : h_team, "H_SCORE" : h_score, #dictionary data is created
                        "AWAY" : a_team, "A_SCORE" : a_score}
                
                df = pd.DataFrame(data) # dictionary data is turned into database and is stored under the variable df
                empty = ""
                teams_played_today = {"HOME" : h_team, "  VS" : empty, #dictionary is created for final display VS is added between home and away stats with an empty strinf so nothing prints in the VS column
                                      "AWAY" : a_team}
                
                ddf = pd.DataFrame(teams_played_today) #dictionary teams_played_today is turned into database
                print(ddf)
                if df.empty:
                    print("sorry please enter a valid date")
                else:
                    break
            
            else: 
                print("please enter a valid date bewtween start of season and last night")
         
            
        
          
        else:
            print("please enter a date within the start ot the season and the current day")
    
    elif choi == "last night": #sets conditions for when input is equal tp last night
        base_url = "http://www.espn.com/nba/scoreboard/_/date/" # url of website without date( this date automaticaly sets to the current day) set under variable base_url
        yesterday = date.today() - timedelta(1)# sets variable for yesterday (today -1)
        yes = (yesterday.strftime('20%y%m%d'))#prints yesterday in yyyymmdd format
        yes = str(yes)# changes yesterday date that is held under the variable yes to a string
        final_url = (base_url + yes) #sets variable final_url equal to the sum of the base_url and yes (yesterdays date yyyymmdd) combines them to create one string
        url = final_url # the final sum is storeed unnder varibale url
        r = requests.get(url) # this function packages the request sends the request to the http server and gets the response 
        html_doc=r.text # returns html response to text under the variable htlm_doc
    
    
        team_names_junk = [] 
        			 
        def find_teams(doc):
            start = doc.find('shortDisplayName')
            start = start + 18
            end = start + 50
            terminate = doc.find('</head>')
            
            name = doc[start:end]
            name_list = name.split(',')
            name = name.replace(" ", "")
            team = name_list[0].strip('"')
            team_names_junk.append(team)
            if end < terminate:
                find_teams(doc[end:])
            else:
                print("")
        
        find_teams(html_doc)
        
        team_list = []
        for team in team_names_junk:
            try:
                if team in teams:
                    team_list.append(team)
                    
            except IndexError:
                print("")
        
        team_scores = []
        
        def find_team_score(doc):
            start = doc.find('homeAway')
            
            end = start + 40
            terminate = doc.find('</head>')
            
            sc = doc[start:end]
        
            sc_list = sc.split(',')
            sco = sc_list[1]
            scor = sco.split(':')
            score = scor[-1].strip('"')
            score = int(score) 
            team_scores.append(score)
            if end < terminate:
                find_team_score(doc[end:])
            else:
                print("")
                
        
                
        find_team_score(html_doc)
        
        for i in team_scores:
            if i == "" or i < 36:
                team_scores.remove(i)
            elif len(team_list) != len(team_scores):
                team_scores.pop()
                
        
                
        h_team, a_team, h_score, a_score = [],[],[],[]
        
        def match_data(teams,scores):
            """inputs are lists"""
            for i in range(0,len(scores),2):
                h_team.append(teams[i])
                a_team.append(teams[i+1])
                h_score.append(scores[i])
                a_score.append(scores[i+1])
            if len(teams) != len(scores):
                print("there is a missmatch somewhere")
                
        match_data(team_list,team_scores)
        
        data = {"HOME" : h_team, "H_SCORE" : h_score, 
                "AWAY" : a_team, "A_SCORE" : a_score}
        
        df = pd.DataFrame(data)
        empty = ""
        teams_played_today = {"HOME" : h_team, "  VS" : empty,
                              "AWAY" : a_team}
        
        ddf = pd.DataFrame(teams_played_today)
        print("here are last nights games")
        print(ddf)
        if ddf.empty:
            print("Sorry, there were no games last night")
            break
        break
    
    else:
        print("type last night for last nights scores or type season day for the scores of a day in the season") 
        
   
Continue = True
while(Continue):
    if ddf.empty:
        break
    choice = input("select the game you would like to view the score of by typing one of the names of the teams in the game")
   #sets conditions for input "choice" 
    if choice in h_team: #if the user input is in the list h_teams it will print the dataframe index that the team is in
        print(df[df["HOME"]== choice])
        break# ends while loop if cindition above is true
    elif choice in a_team: #if the user input is in a_team list it will print the dataframe index that the team is in
        print(df[df["AWAY"]== choice])
        break #ends while loop if condition above is true
    elif choice in teams and choice not in a_team or choice in teams and choice not in h_team:
        print("sorry that team did not play last night")
            #condition above checks to see if the input etered is in the list of all the teams (teams ) but it is not in h_team or a_team 
    
    else: # if none of these conditions are true the statement below will be printed 
        print("typing error, please enter the name of a team from the game")


while(Continue):   #while loop created
    if ddf.empty:
        break
    choice2 = input("would you like to see the scores from another game? yes or no?")
    
    if choice2 == "yes": # sets conditions if user input is equal to yes
        print("here are last nights games")
        print(ddf) #prints database with all games
        while(Continue):
            choice = input("select the game you would like to view the score of by typing one of the names of the teams in the game")

            if choice in h_team: # if the user input is in the list h_teams it will print the dataframe index that the team is in
                print(df[df["HOME"]== choice])
                break# ends while loop if cindition above is true
            elif choice in a_team: #if the user input is in a_team list it will print the dataframe index that the team is in
                print(df[df["AWAY"]== choice])
                break #ends while loop if condition above is true
            elif choice in teams and choice not in a_team or choice in teams and choice not in h_team:
                print("sorry that team did not play last night")
            else: # if none of these conditions are true the loop while continnue and will print the staement  below
                print("typing error, please enter the name of a team from the game")
    elif choice2 == "no": # sets conditions if user input is equal to no
        print("ok, thank you for using NBA game review")
        break #ends while if user input is equal to no and prints the statement above 
   
             
    else: # if none of the conditoins are true the loop will continue 
        print("tyrping error please enter yes or no")
        
        
        

        


