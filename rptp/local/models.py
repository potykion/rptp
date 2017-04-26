import json

from rptp.common.models import ActressProxy


class ActressManager(ActressProxy):
    def fetch(self):
        with open('data/actresses.json') as f:
            return json.load(f)

    def serialize(self, actress):
        return actress
