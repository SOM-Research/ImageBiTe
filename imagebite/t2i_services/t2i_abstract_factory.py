class T2IFactory:

    def __init__(self):
        self.__builders = {}

    def register_builder(self, key, builder):
        self.__builders[key] = builder

    def create(self, key, **kwargs):
        builder = self.__builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)