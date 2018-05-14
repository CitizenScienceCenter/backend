
class CSBase():

    def dump(self):
        return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])