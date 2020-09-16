import random
import string


class randomStr(object):
    def __init__(self):
        self.letters = string.ascii_letters+string.digits

    def getRandomStr(self):
        """ Return randrom String, len = 6 """
        return((''.join(random.choice(self.letters) for i in range(6))))
