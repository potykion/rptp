import random


class ActressProxy:
    def fetch(self):
        raise NotImplementedError

    def serialize(self, actress):
        raise NotImplementedError

    def fetch_as_json(self):
        return list(map(self.serialize, self.fetch()))

    def generate_actress(self):
        actresses = self.fetch_as_json()
        return random.choice(actresses)['name']
