import os
import sys

root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, 'site-packages.tar.gz'))

import sae
from microblog import create_app

app = create_app('microblog.config.SAEConfig')

application = sae.create_wsgi_app(app)
