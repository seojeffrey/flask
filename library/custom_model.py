
class EasyModel:
    def __init__(self, **kwargs):
        super().__init__()
        self.__dict__.update(kwargs)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
