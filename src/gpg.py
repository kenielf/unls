# <!-- Imports -->
from typing import Union
from os import getenv, PathLike
from subprocess import run, CompletedProcess
from log import debug, error

# <!-- Code -->
GPG_CMD: str = getenv("GPG_CMD", "gpg")

# Decrypts gpg encrypted files and return its contents as a str
def decrypt(_path: Union[str, bytes, PathLike]) -> str:
    output: CompletedProcess = run(
        [GPG_CMD, "-dq", _path],
        capture_output=True, text=True
    )
    if output.returncode != 0:
        error(f"Failed to decrypt file '{_path}'", 1)
    else:
        debug(f"Successfully decrypted file '{_path}'")
    return output.stdout.strip()

# Encrypt
def encrypt(content: str, _path: Union[str, bytes, PathLike]) -> None:

    pass

