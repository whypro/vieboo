# -*- coding: utf-8 -*-

from microblog import create_app

app = create_app('microblog.config.LocalDevelopmentConfig')

if __name__ == '__main__':
    app.run(host='0.0.0.0')

