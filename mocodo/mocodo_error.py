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
    return MocodoError(1457, f"Invalid sub-argument: {subsubopt}={subsubarg}.")

def subsubopt_error(subsubopt):
    return MocodoError(1458, f"Invalid sub-sub-option: {subsubopt}.")