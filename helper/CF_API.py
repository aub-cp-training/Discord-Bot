import codeforces_api, requests, re, time
from cDatabase.DB_Users import DB_Users
from helper.cTime import get_in_date_format

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

database_users = DB_Users('db_users')
cf_api = codeforces_api.CodeforcesApi()

def get_cf_statistics(handle):
    driver = webdriver.Firefox()
    url = "https://a2oj.netlify.app/codeforces.html?handle=" + handle
    driver.get(url)
    time.sleep(8) 
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    
    ids = ['tried', 'solved', 'averageAttempt', 'solvedWithOneSub', 'maxAttempt']
    ids += ['maxAc', 'contestCount', 'best', 'worst', 'maxUp', 'maxDown']

    tags = soup.find_all(id= ids)

    mp = {}
    
    for i in range(len(ids)): mp[ids[i]] = tags[i].string

    driver.close()

    return mp

# ------------------------------------ { CF_API } ------------------------------------ # 
class CF_API():
    # ------------------ [ user_info() ] ------------------ # 
        # Returns information of the user
    def user_info(self, user): return cf_api.user_info([user.handle])[0]

    # ------------------ [ user_status() ] ------------------ # 
        # Returns the status of the user
    def user_status(self, user): return cf_api.user_status(user.handle)

    # ------------------ [ user_rating() ] ------------------ # 
        # Returns the current CodeForces rating of the user
    def user_rating(self, handle):
        lst = cf_api.user_info([handle])[0]
        return lst.rating

    # ------------------ [ contest_rating_changes() ] ------------------ # 
        # Returns the user's "rank", "handle", "old_rating", "new_rating" from "contest"
    def contest_rating_changes(self, contest_id):
        try:
            lst = cf_api.contest_rating_changes(contest_id)
            arr = database_users.values()
            result = []
            contest = str()
            for user in lst:
                if len(contest) == 0: contest = user.contest_name
                if not user.handle in arr: continue
                result.append((user.rank, user.handle, user.old_rating, user.new_rating))
                result.sort()
            return result, contest
        except Exception: return None

    # ------------------ [ solved_problems() ] ------------------ # 
        # Checks if the problem's verdict was "OK" before counting it
        # Returns problems solved from "problemset", "gym", and "total" = "problemset" + "gym"
    def solved_problems(self, user):
        d = {}
        solved = set()
        total = gym = 0

        for prob in self.user_status(user):
            if prob.verdict != "OK": continue

            try: id = str(prob.problem.contest_id) + prob.problem.index
            except: 
                try: id = str(prob.problem.problemset_name) + prob.problem.index
                except: continue

            if id in solved: continue
            solved.add(id)

            if prob.problem.rating == None:
                gym += 1
                continue

            total += 1
            index = prob.problem.index.strip('1234567890')
            if d.get(index): d[index] += 1
            else: d[index] = 1

        return {'total': total + gym, 'problemset': total, 'gym': gym, 'problems': sorted(d.items())}

    # ------------------ [ solved_ratings() ] ------------------ # 
        # Checks if the problem's verdict was "OK" before counting it
        # Returns the number of problems solved by the user at each difficulty rating
    def solved_ratings(self, user):
        d = {}
        solved = set()

        for prob in self.user_status(user): 
            if prob.verdict != "OK": continue

            try: id = str(prob.problem.contest_id) + prob.problem.index
            except: 
                try: id = str(prob.problem.problemset_name) + prob.problem.index
                except: continue

            if id in solved: continue
            solved.add(id)

            if prob.problem.rating == None: continue

            index = prob.problem.rating
            if d.get(index): d[index] += 1
            else: d[index] = 1

        return list(d.items())

    # ------------------ [ user_rank() ] ------------------ # 
        # Returns the user's CodeForces rating, if not available then Inactive
    def user_rank(self, user):
        rating = self.user_rating(user.handle)
        if (rating == None): return "Inactive"
        if (rating < 1200): return "Newbie"
        if (rating < 1400): return "Pupil"
        if (rating < 1600): return "Specialist"
        if (rating < 1900): return "Expert"
        if (rating < 2200): return "Candidate Master"
        if (rating < 2300): return "Master"
        if (rating < 2400): return "International Master"
        if (rating < 2600): return "Grandmaster"
        if (rating < 2900): return "International Grandmaster"
        return "Legendary Grandmaster"

    def is_valid_handle(self, handle):
        try:
            self.user_rating(handle)
            return True
        except Exception:
            return False

    def multiple_user_ratings(self, lst):
        arr = []

        for i in range(len(lst)):
            if i != 0 and i % 5 == 0: time.sleep(0.2)
            arr.append((lst[i], self.user_rating(lst[i])))

        return arr

    def codeforces_contests(self):
        response = requests.get("https://codeforces.com/contests")
        result = [i.start() for i in re.finditer("table", response.text)]
        if (len(result) < 8): return {}
        x = response.text[result[6] : result[7]]

        result = [i.start() for i in re.finditer("data-contestId=", x)]
        lst = {}
        for i in range(len(result)):
            st = str()
            if i + 1 < len(result): st = x[result[i] : result[i + 1]]
            else: st = x[result[i]:]
            arr = [i.start() for i in re.finditer('<td class="state">', st)]
            st = st[ : arr[0]]

            _id = st[16 : 20]

            arr = [i.start() for i in re.finditer('td', st)]
            name = st[arr[0] + 5 : arr[1] - 8]

            duration = st[arr[len(arr) - 2] + 13 : arr[len(arr) - 1] - 8] 

            arr = [i.start() for i in re.finditer('data-locale', st)]
            time = get_in_date_format(st[arr[0] + 17 : arr[0] + 34])

            lst[_id] = {'name': name, 'date': time, 'duration': duration}

        return lst

    def get_statistics(self, handle):
        driver = webdriver.Firefox()
        url = "https://a2oj.netlify.app/codeforces.html?handle=" + handle
        driver.get(url)
        time.sleep(8) 
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
    
        ids = ['tried', 'solved', 'averageAttempt', 'solvedWithOneSub', 'maxAttempt']
        ids += ['maxAc', 'contestCount', 'best', 'worst', 'maxUp', 'maxDown']

        tags = soup.find_all(id= ids)

        mp = {}
    
        for i in range(len(ids)): mp[ids[i]] = tags[i].string

        driver.close()

        return mp