from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

from lfProd.models import initialize_sql


def db(request):
    maker = request.registry.dbmaker
    session = maker()

    def cleanup(request):
        if request.exception is not None:
            session.rollback()
        else:
            session.commit()
        session.close()
    request.add_finished_callback(cleanup)

    return session

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.include('.routes')

        # https://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/
        # database/sqlalchemy.html#importing-all-sqlalchemy-models
        config.scan('lfProd.models')  # the "important" line
        engine = engine_from_config(settings, 'sqlalchemy.')
        initialize_sql(engine)
        config.registry.dbmaker = sessionmaker(bind=engine)
        config.add_request_method(db, reify=True)

        config.scan()
    return config.make_wsgi_app()
