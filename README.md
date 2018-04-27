# RPTP

Watch random adult videos from VK.

# Installation

## Dependencies

To install dependencies:
```
pip install -r requirements.txt
```

## Sanic

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

# Run

To run tests or app:

1. Set envs: VK_APP_ID, VK_CLIENT_SECRET, MONGO_URL