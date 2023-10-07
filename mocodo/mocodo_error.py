import textwrap


class MocodoError(Exception):
    def __init__(self, errno, message):
        message = f"Mocodo Err.{errno} - {message}"
        message = "\n".join(
            [
                "\n".join(
                    textwrap.wrap(
                        line,
                        88,
                        break_long_words=False,
                        replace_whitespace=False,
                    )
                )
                for line in message.splitlines()
                if line.strip() != ""
            ]
        )
        self.errno = errno
        super(MocodoError, self).__init__(message)

def subarg_error(subsubopt, subsubarg):
    return MocodoError(19, _('Invalid sub-argument: "{subsubopt}={subsubarg}".').format(subsubopt=subsubopt, subsubarg=subsubarg))  # fmt: skip

def subsubopt_error(subsubopt):
    return MocodoError(20, _('Invalid sub-sub-option: "{subsubopt}".').format(subsubopt=subsubopt))  # fmt: skip

def subopt_error(opt, subopt):
    raise MocodoError(21, _('Unknown "{opt}" sub-option: "{subopt}".').format(opt=opt, subopt=subopt))  # fmt: skip
