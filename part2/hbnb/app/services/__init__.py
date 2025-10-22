from flask import current_app
from .facade import HBnBFacade

class LazyFacade:
    """
    Façade qui s'initialise paresseusement avec les repositories de l'application.
    """
    def __init__(self):
        self._facade = None

    def __getattr__(self, name):
        if not self._facade:
            repositories = current_app.config.get('repositories')
            self._facade = HBnBFacade(repositories)
        return getattr(self._facade, name)

facade = LazyFacade()

__all__ = ['facade']
