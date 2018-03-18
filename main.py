import os

from rptp.app import app

if __name__ == '__main__':
    app.run(
        os.getenv('HOST', '0.0.0.0'),
        int(os.getenv('PORT', '8000'))
    )
