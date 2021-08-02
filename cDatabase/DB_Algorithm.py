import importlib
from cDatabase.KV_Database import KV_Database

def get_next_id(mx_id):
    _id = str(int(mx_id) + 1)
    while len(_id) < 5: _id = "0" + _id
    return _id


class DB_Algorithm(KV_Database):
    def __init__(self, path): 
        super().__init__(path)
        file_path = '.'.join(self.path.split('/'))[:-3]
        try:
            db = importlib.import_module(file_path)
            self.mp = db.Mapping
            self.inv = db.Inverse
        except Exception as ex:
            fs = open(self.path, "a")
            fs.write("\n\nMapping = {}")
            fs.write("\n\nInverse = {}")
            fs.close()
            self.mp, self.inv = {}, {}

    def save(self):
        file = open(self.path, "w")
        file.write("DataBase = " + str(self.db))
        file.write("\n\nMapping = " + str(self.mp))
        file.write("\n\nInverse = " + str(self.inv))
        file.close()

    def find_algo(self, algo):
        if len(algo._id) == 0: return False
        if algo.lang not in self.db[algo._id]['lang_zip'].keys(): return False
        return True
    
    def add_algo(self, algo):
        if len(algo._id) != 0:
            self.db[algo._id]['lang_zip'][algo.lang] = algo.is_zip
        else: 
            mx_id = max(list(self.db.keys()) + ['00000'])
            _id = get_next_id(mx_id)
            self.db[_id] = {
                'algo': algo.algo,
                'lang_zip': {
                    algo.lang: algo.is_zip
                }
            }
            self.inv[algo.algo] = _id
        
        self.save()
        return True

    def get_id_of_algo(self, algo):
        return self.inv[algo]

    def get_algo_with_id(self, _id):
        return ""

    def get_langs(self, algo):
        return list(self.db[algo._id]['lang_zip'].keys())

    def delete_algo(self, algo):
        del(self.db[algo._id]['lang_zip'][algo.lang])

        if len(self.db[algo._id]['lang_zip']) == 0:
            del(self.db[algo._id])
            del(self.inv[algo.algo])
            if algo._id in self.mp.keys(): del(self.mp[algo._id])

        self.save()
        return True

    def find_mapping(self, algo, alias):
        if algo._id not in self.mp.keys(): return False
        if alias not in self.mp[algo._id]: return False
        return True

    def add_mapping(self, algo, alias):
        if self.find_mapping(algo, alias): return False

        if algo._id in self.mp.keys(): self.mp[algo._id] += [alias]
        else: self.mp[algo._id] = [alias]

        self.save()

        return True

    def get_mappings(self, algo):
        if algo._id in self.mp.keys(): return self.mp[algo._id]
        else: return []

    def is_valid_mapping(self, algo, keyword):
        keyword = keyword.lower()
        if keyword in algo.algo: return True
        for alias in self.get_mappings(algo):
            if keyword in alias: return True
        return False