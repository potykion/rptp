# RPTP

Watch random adult videos from VK.

# Installation

## Dependencies

To install dependencies:
```
pip install -r requirements.txt
```

### Sanic

To install Sanic on Windows:

1. Clone Sanic [repo](https://github.com/channelcat/sanic):
```
git clone https://github.com/channelcat/sanic.git
```

2. Set envs:
```
set SANIC_NO_UVLOOP=true
set SANIC_NO_UJSON=true
```

3. Install from source:
```
cd sanic
pip install .
```

### Pre-commit hooks

Install pre-commit hooks via:
```
pre-commit install
```

# Run

To run tests or app:

1. Set envs:
- VK_APP_ID - vk application id (can be found in vk app settings)
- VK_CLIENT_SECRET - vk secure key (can be found in vk app settings)
- MONGO_URL - mongodb connection string
- MONGO_DB - mongodb database name

2. Run:

To run tests:
```
pytest tests
```

To run app:
```
python main.py
```

# References

- [VK API](https://vk.com/dev/methods)
- [Sanic API](http://sanic.readthedocs.io/en/latest/)
- [Motor API](https://motor.readthedocs.io/en/stable/tutorial-asyncio.html)
- [PyMongo API](https://api.mongodb.com/python/current/tutorial.html)