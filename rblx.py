from requests import exceptions, get, post
from misc_classes import * #Imports classes like ThumnailConfig n shit
from logging import warning, info
global loggedInAs
loggedInAs = None #The Client object that is currently logged in
useproxy = True

def makeRequest(requestType:str, endpoint:str,prefix:str="www", arguments:list=[], headers:dict={}, data:dict={}, proxy:bool=False):
    """An internal function that makes a request to the provided endpoint
requestType (string): The type of request to make (`GET, POST` are supported)
endpoint (string): The endpoint to make the request to (I.E, users/inventory)
prefix (string): the subdomain to request to
*arguments (list): The arguments appended to the url (`['userid=767877034', 'limit=100']`)
*headers (dict): HTTP headers sent with the request
*data (dict): Any data that's sent with the request
*proxy (bool): Will a proxy be used instead of roblox.com?

*optional
    """
    if requestType != "POST" and requestType != "GET":
        raise Exception("Invalid request type. Valid requests are: POST, GET (case sensitive)")
    domain = "roblox.com"
    if proxy == True or useproxy == True:
        domain = "roproxy.com"
    url = f"https://{prefix}.{domain}/{endpoint}"
    for i,x in enumerate(arguments):
        if i == 0:
            url+=f"?{x}"
        else:
            url+=f"&{x}"
    try:
        if requestType == "GET":
            return get(url=url, headers=headers, data=data)
        else:
            return post(url=url, headers=headers, data=data)
    except Exception as e:
        print("Error fetching data from roblox: ",e)
        return None

class User:
    """A container for a Roblox account that is not currently authenticated"""
    id = 0
    name = ""
    displayName = ""
    description = ""
    banned = False,
    verifiedBadge = True,
    created = ""
    usernameHistory = []
    def send_message(self, subject:str, body:str):
        """Sends one of the older email style messages to the user using the currently logged in credentials"""
        if loggedInAs != None:
            print(loggedInAs.token)
            req = makeRequest("POST", "v1/messages/send", "privatemessages", headers={'Cookie': f".ROBLOSECURITY={loggedInAs.token}"}, data={
                'subject': subject,
                'body': body,
                'recipientid': self.id
            })
            if req.status_code == 200:
                return
            else:
                raise Exception(f"Roblox returned {req.status_code}: {req.json()}")
        else:
            raise Exception("You are not logged in with a ROBLOSECURITY token!")

    def get_avatar_headshot(self, size:ThumbnailSize=ThumbnailSize.x420, format:ImageFormat=ImageFormat.png, isCircular:bool=False):
        """Gets the url for the avatar headshot for the user
        
        size: (ThumbnailSize) The size (In pixels) of the thumbnail
        format: (ImageFormat) The image format (png/jpeg/webp accepted)
        isCircular: (bool) Is the output image circular?"""
        req = makeRequest("GET", "v1/users/avatar-bust", "thumbnails", [f'userIds={str(self.id)}', f'size={size}', f'format={format}', f'isCircular={str(isCircular).lower()}'])
        if req.status_code == 200:
            return req.json()['data'][0]['imageUrl']
        else:
            raise Exception(f"Roblox returned {req.status_code}")
    def get_avatar_bust(self, size:ThumbnailSize=ThumbnailSize.x420, format:ImageFormat=ImageFormat.png, isCircular:bool=False):
        """Gets the url for the avatar bust for the user
        
        size: (ThumbnailSize) The size (In pixels) of the thumbnail
        format: (ImageFormat) The image format (png/jpeg/webp accepted)
        isCircular: (bool) Is the output image circular?"""
        req = makeRequest("GET", "v1/users/avatar-headshot", "thumbnails", [f'userIds={str(self.id)}', f'size={size}', f'format={format}', f'isCircular={str(isCircular).lower()}'])
        if req.status_code == 200:
            return req.json()['data'][0]['imageUrl']
        else:
            raise Exception(f"Roblox returned {req.status_code}")
    def get_avatar(self, size:ThumbnailSize=ThumbnailSize.x420, format:ImageFormat=ImageFormat.png, isCircular:bool=False):
        """Gets the url for the user's fullbody avatar
        
        size: (ThumbnailSize) The size (In pixels) of the thumbnail
        format: (ImageFormat) The image format (png/jpeg/webp accepted)
        isCircular: (bool) Is the output image circular?"""
        req = makeRequest("GET", "v1/users/avatar", "thumbnails", [f'userIds={str(self.id)}', f'size={size}', f'format={format}', f'isCircular={str(isCircular).lower()}'])
        if req.status_code == 200:
            return req.json()['data'][0]['imageUrl']
        else:
            raise Exception(f"Roblox returned {req.status_code}")

class Client(User):
    """The Roblox account you're logged in to \nROBLOSECURITY: The account's ROBLOSECURITY token, including the warning"""
    def __init__(self, ROBLOSECURITY:str):
        self.token = ROBLOSECURITY
        req = makeRequest("GET", "v1/users/authenticated", "users", headers={'Cookie': f".ROBLOSECURITY={self.token}", 'accept':'application/json'})
        if req.status_code == 200:
            self.id = req.json()['id']
            self.name = req.json()['name']
            self.displayName = req.json()['displayName']

            req2 = makeRequest("GET", f"v1/users/{str(req.json()['id'])}","users")
            if req2.status_code == 200:
                resJson = req2.json()
                self.description = resJson['description']
                self.banned = resJson['isBanned'],
                self.verifiedBadge = resJson['hasVerifiedBadge']
                self.created = resJson['created']
            global loggedInAs
            loggedInAs = self
            print(f"Logged in using ROBLOSECURITY cookie")
        elif req.status_code == 401:
            raise Exception("The token you provided is invalid!")

def getUser(userId:int):
    """Returns a **user** object with all of the account's public information"""
    req = makeRequest("GET", f"v1/users/{str(userId)}","users")
    if req.status_code == 200:
        resJson = req.json()
        user = User()
        user.id = userId
        user.name = resJson['name']
        user.displayName = resJson['displayName']
        user.description = resJson['description']
        user.banned = resJson['isBanned'],
        user.verifiedBadge = resJson['hasVerifiedBadge']
        user.created = resJson['created']

        req2 = makeRequest("GET", f"v1/users/{str(userId)}/username-history","users", ['limit=100', 'sortOrder=Asc'])
        if req2.status_code == 200:
            user.usernameHistory = []
            for x in req2.json()['data']:
                user.usernameHistory.append(x['name'])
            
        return user
    elif req.status_code == 404:
        raise Exception("Userid is not valid")
    
class Group:
    """The container for a group"""
    id = None #Int
    name = None #string
    owner = None #Class User()
    iconUrl = None #string
    shout = None #dict, {"poster": user, "content": string, "time": datetime.datetime}

def getGroup(groupId:int):
    pass