import sae

from microblog import create_app

app = create_app('microblog.config.SAEConfig')

application = sae.create_wsgi_app(app)
