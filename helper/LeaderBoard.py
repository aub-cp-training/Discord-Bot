from helper.cEmbed import granted_msg, denied_msg

class LeaderBoard():
   def Standings(self, lst):
        i = 1
        ids = handles = ratings = ""
        for (h, r) in sorted(lst, key = lambda x: x[1], reverse = True):
            ids += "**" + str(i) + "**" +'\n'
            if i == 1: handles += h + ":crown:" + "\n"
            else: handles += h + "\n"
            ratings += str(r) + "\n"
            i += 1

        if len(ids) == 0: return denied_msg("Warning", "The Leaderboard is Still Empty.")

        response = granted_msg("CodeForces Standings")

        response.add_field(name = "#", value = ids, inline = True)
        response.add_field(name = "Handle", value = handles, inline = True)
        response.add_field(name = "Rating", value = ratings, inline = True)

        return response
