import logging
from importlib import import_module
from pkgutil import walk_packages

from core import hints

log = logging.getLogger(__name__)


class PackageLoader:
    @classmethod
    def load_package(cls, package: str):
        log.debug('importing package %s', package)
        package = import_module(package)

        for loader, name, is_pkg in walk_packages(package.__path__):
            full_name = f'{package.__name__}.{name}'
            log.debug('importing module %s', full_name)
            import_module(full_name)

            if is_pkg:
                cls.load_package(full_name)

    @classmethod
    def load_packages(cls, packages: hints.Packages):
        for package in packages:
            cls.load_package(package)
