from cDatabase.DB_Algorithm import DB_Algorithm
from helper.GitHub import GitHub
import requests, json

github_api = GitHub()
db_algo = DB_Algorithm('db_algorithms')
config = json.load(open('config.json', 'r'))

class Algorithm():
    _id = str()
    algo = str()
    lang, is_zip = str(), bool()
    lang_zip = list()
    code = str()
    output_path = config['module_cmds_loc'] + "/algo/" + config['temp_file']
 
    def __init__(self, 
        _id= str(), 
        str_algo= str(),
        algo= str(), lang= str(), code= str(), is_zip= bool()
    ):
        if len(_id) != 0:
            mp = db_algo.get(_id)
            self._id = _id
            self.algo, self.lang_zip = mp['algo'], sorted(list(mp['lang_zip'].items()))
            self.lang = lang
            if self.lang in self.get_langs(): self.is_zip = db_algo.db[self._id]['lang_zip'][self.lang]
        elif len(str_algo) != 0:
            args = str_algo.split('.')
            if len(args) == 1: args.append('-')
            if args[-1] == 'zip': args, self.is_zip = args[0].split("__"), True
            self.algo, self.lang = args[0].lower(), args[1].lower()
            if self.algo in db_algo.inv.keys(): self._id = db_algo.get_id_of_algo(self.algo)
        else:
            self.algo, self.lang = algo.lower(), lang.lower()
            self.code, self.is_zip = code, is_zip

            if self.algo in db_algo.inv.keys(): self._id = db_algo.get_id_of_algo(self.algo)
            if self.lang in self.get_langs(): self.is_zip = db_algo.db[self._id]['lang_zip'][self.lang]

    def __str__(self):
        if self.is_zip: return self.algo + "__" + self.lang + ".zip"
        return self.algo + "." + self.lang

    def is_found(self):
        if len(self._id) == 0: return False
        return self.lang in self.get_langs()

    def add(self):
        if self.is_found(): return False
        return db_algo.add_algo(self)

    def delete(self):
        if not self.is_found(): return False
        return db_algo.delete_algo(self)

    def map_to(self, alias):
        return db_algo.add_mapping(self, alias)

    def get_mappings(self):
        return db_algo.get_mappings(self)

    def is_valid_mapping(self, keyword):
        return db_algo.is_valid_mapping(self, keyword)

    def get_langs(self):
        if len(self._id) == 0: return []
        return db_algo.get_langs(self)

    def get_code_path(self):
        if self.is_zip:
            file_path = self.output_path + ".zip"
            url = github_api.get_zip(str(self))
            r = requests.get(url)
            with open(file_path, 'wb') as f: f.write(r.content)
        else:
            code = github_api.get_file(str(self))
            file_path = self.output_path + ".txt"
            # adding extra "new-line" chars
            with open(file_path, 'w') as f: 
                for line in code.split('\n'): f.write(line)
        return file_path

    async def write_file(self, attts):
        extension = attts.filename.split(".")[-1]

        if extension == 'zip': file_path = self.output_path + ".zip"
        else: file_path = self.output_path + ".txt"
        await attts.save(file_path)


        algo = Algorithm()
        return extension

    def commit(self):
        file_path = self.output_path + (".zip" if self.is_zip else ".txt")
        with open(file_path, 'rb') as f: code = f.read()
        return github_api.add_file(str(self), code)

    def all(self):
        lst = []
        for (_id, full) in db_algo.items():
            algo = Algorithm(algo= full['algo'])
            for (lang, zp) in full['lang_zip'].items():
                algo.lang, algo.is_zip = lang, zp
                lst.append(str(algo))
        return lst 
