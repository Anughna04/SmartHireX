class Shortlister:
    def __init__(self, threshold=80):
        self.threshold = threshold

    def shortlist(self, candidates):
        return [c for c in candidates if c["match"] >= self.threshold]