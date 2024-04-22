from requests import exceptions, get, post
from misc_classes import * #Imports classes like ThumnailConfig n shit

    

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
    if proxy == True:
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
        return user
    elif req.status_code == 404:
        raise Exception("Userid is not valid")