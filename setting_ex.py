class User:
    def __init__(self, gameName, tag, reg) -> None:
        self.gameName = gameName
        self.tag = tag
        self.reg = reg
        
# set these values to your own then change to settings.py
API_KEY = "example key"
query = User("name", "tag", "region")