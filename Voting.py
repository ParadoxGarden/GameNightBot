class Voting:
    vote_data = dict()
    vote_data["emojivotes"] = dict()
    vote_data["useremojis"] = dict()

    def add_vote(self, user, emoji):
        useremojis = self.vote_data["useremojis"]
        emojivotes = self.vote_data[""]

    def clear_vote(self, user):
        for emoji in self.vote_data["useremojis"].get(user):
            return


# invert number in list for vote
def numerical_inverse(number):
    if number == 1:
        return 3
    elif number == 2:
        return 2
    elif number == 3:
        return 1
