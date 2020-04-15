import json


class Config():
    _dict = {
        'curProgram': 0,
        'rgb': [255, 255, 255],
        'brightness': 50,
        'rate': 10
    }
    _unsaved = False

    @classmethod
    def save(cls):
        if cls._unsaved:
            print('Saving the config')
            with open('config.json', 'w') as file:
                json.dump(cls._dict, file)
            cls._unsaved = False

    @classmethod
    def load(cls):
        try:
            with open('config.json') as file:
                cls._dict = json.load(file)
            return True
        except (OSError, ValueError):
            print('Cannot open config, generating a new configuration file...')
            cls._unsaved = True
            cls.save()
            return False

    @classmethod
    def cur_program(cls, value=None):
        if value is not None:
            cls._dict['curProgram'] = value
            cls._unsaved = True
        return cls._dict['curProgram']

    @classmethod
    def rgb(cls, value=None):
        if value is not None:
            cls._dict['rgb'] = value
            cls._unsaved = True
        return cls._dict['rgb']

    @classmethod
    def red(cls, value=None):
        if value is not None:
            cls._dict['rgb'][0] = value
            cls._unsaved = True
        return cls._dict['rgb'][0]

    @classmethod
    def green(cls, value=None):
        if value is not None:
            cls._dict['rgb'][1] = value
            cls._unsaved = True
        return cls._dict['rgb'][1]

    @classmethod
    def blue(cls, value=None):
        if value is not None:
            cls._dict['rgb'][2] = value
            cls._unsaved = True
        return cls._dict['rgb'][2]

    @classmethod
    def brightness(cls, value=None):
        if value is not None:
            if value > 100:
                value = 100
            elif value < 0:
                value = 0
            cls._dict['brightness'] = int(value)
            cls._unsaved = True
        return cls._dict['brightness']

    @classmethod
    def rate(cls, value=None):
        if value is not None:
            cls._dict['rate'] = value
            cls._unsaved = True
        return cls._dict['rate']
