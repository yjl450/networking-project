# Computer Networking Midterm Project
By Yijian Liu (@yjl450), Leyi Sun

# Communication Format
## Create new user (login)
client: send 
    
    {"action": "newuser", "username": *username*}

server: reply 
    
    {"action":"newuser", "result": *success or other error*, "userid": *userid*, "username": *username*}

userid is generated by the server and the last digit is 0

## Update contact list

Server: send

    {"action": "contact",
     "contact":
        {"person": {
            *userid*:{*userid*: *username*}
            },
        "group": {
            *groupid*: {*userid*: *username*}
            }  
        }
    }

## Send message to group
Client: send 
    
    {"action": "message", "sender": *userid*, "receiver": *groupid*, "message": *content*}

Server: forward the message to all members of the group (excluding sender) 
    
    {"action": "message", "sender": *userid*, "receiver": *groupid*, "message": *content*}

## Create Group
client: send

    {"action": "newgroup", 
     "sender": *userid*, 
     "member":{*userid*: *username*}} // including sender
Server: update contact list 

## Join Group
client: send 

    {"action": "join", "groupid": *groupid*, "sender": *userid*}
Server: remove user from person list, update contact list

## Leave Group
client: send 

    {"action": "leave", "groupid": *groupid*, "sender": *userid*}
Server: remove user from group. If there is only one user in the group, delete the group, then update contact list

## Logout
client: send

    {"action": "logout", "sender": *userid*}

Server: delete current user from all possible groups, delete user from person list, update contact list

