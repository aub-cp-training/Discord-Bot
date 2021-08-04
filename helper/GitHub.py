import requests, json
from github import Github

config = json.load(open('config.json', 'r'))

class GitHub():
    path = "https://raw.githubusercontent.com/"
    zip_path = "https://github.com/"
    username = str()
    repository = str()
    branch = str()
    GitHub_Client = None
    GitHub_Repo = None
  
    def __init__(self, username = 'aub-cp-training', repository = 'Algorithms', branch = 'main'):
        self.username, self.repository, self.branch = username, repository, branch
        self.path += username + "/" + repository + "/" + branch + "/"
        self.zip_path += username + "/" + repository + "/raw/" + branch + "/"

    def init_api(self):
        if self.GitHub_Client == None: self.GitHub_Client = Github(config['GitHub_Token'])
        if self.GitHub_Repo == None: 
            self.GitHub_Repo = self.GitHub_Client.get_repo(self.username + "/" + self.repository)

    def get_file(self, filename):
        try:
            url = self.path + filename
            return requests.get(url).text
        except Exception: 
            return ""

    def add_file(self, filename, code):
        try:
            self.init_api()
            self.GitHub_Repo.create_file(filename, "API Created " + filename, code, branch= self.branch)
            return True
        except Exception as ex:
            return ex

    def get_all_files(self):
        self.init_api()

        lst = []
        
        contents = self.GitHub_Repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir": contents.extend(self.GitHub_Repo.get_contents(file_content.path))
            else: lst.append(file_content.path)

        return lst

    def delete_file(self, filename):
        try:
            self.init_api()

            contents = self.GitHub_Repo.get_contents(filename)
            self.GitHub_Repo.delete_file(contents.path, "API Deleted " + filename, contents.sha, branch= self.branch)
        except Exception as ex:
            return ex

    def get_zip(self, filename):
        return self.path + filename
