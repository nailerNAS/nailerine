from core.packages import PackageLoader


def load_packages():
    PackageLoader.load_packages(f'modules.{module}'
                                for module
                                in ('anti_flood',
                                    'db_model',
                                    'nailerine',
                                    'nailerine_bot'))
