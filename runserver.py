# -*- coding: utf-8 -*-
import os
import sys
# 将依赖模块文件夹加入系统路径
deps_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'deps')
sys.path.insert(0, deps_path)

from microblog import create_app

app = create_app('microblog.config.DevelopmentBCSConfig')

if 'SERVER_SOFTWARE' in os.environ:
    from bae.core.wsgi import WSGIApplication
    application = WSGIApplication(app)
elif __name__ == '__main__':
    print app.config['USE_BCS_BUCKET']
    app.run()
