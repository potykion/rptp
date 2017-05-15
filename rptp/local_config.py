SECRET_KEY = 'f2c416dafcf647518b4aa91e0d603f7a'

TOKEN = ''

with open('data/token.txt') as f:
    TOKEN = f.readline().strip()
