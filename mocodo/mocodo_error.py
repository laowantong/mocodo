import textwrap

class MocodoError(Exception):
    
    def __init__(self, errno, message):
        message = textwrap.fill("Mocodo Err.%s - %s" % (errno, message), 80)
        self.errno = errno
        super(MocodoError, self).__init__(message)
