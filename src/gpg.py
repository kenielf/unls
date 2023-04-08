# <!-- Imports -->
from typing import Union
from os import getenv, PathLike, path
from subprocess import Popen, PIPE
from log import debug, error

# <!-- Code -->
GPG_CMD: str = getenv("GPG_CMD", "gpg")
GPG_ARGS = [
    GPG_CMD, "--batch", "--yes",
]


# Decrypt the contents using a passphrase, returning a string
def decrypt(encrypted_content: bytes, passphrase: Union[str, None]) -> str:
    # Start the commands pipeline
    if passphrase is not None:
        gpg: Popen = Popen(
            [*GPG_ARGS, "--passphrase", passphrase, "-dq"],
            stdin=PIPE, stdout=PIPE, stderr=PIPE
        )
    else:
        gpg: Popen = Popen(
            [*GPG_ARGS, "-dq"],
            stdin=PIPE, stdout=PIPE, stderr=PIPE
        )
    stdout: bytes = gpg.communicate(encrypted_content)[0]
    # Return the decoded stdout
    return stdout.decode("utf-8", errors="ignore")


# Decrypts the file and return the decrypted stripped contents 
def decrypt_file(_path: Union[str, bytes, PathLike], passphrase: Union[str, None]) -> str:
    # Check if the file exists
    if not path.isfile(_path):
        error("File does not exist!", 1)

    # Read the file and decrypt it
    debug(f"Reading from file: '{_path}'")
    with open(_path, "rb") as file:
        return decrypt(file.read(), passphrase).strip()


# Encrypt the contents using a passphrase and return bytes
def encrypt(content: str, passphrase: str) -> bytes:
    # Start the commands pipeline
    gpg: Popen = Popen(
        [*GPG_ARGS, "--passphrase", passphrase, "--symmetric"],
        stdin=PIPE, stdout=PIPE, stderr=PIPE
    )
    stdout: bytes = gpg.communicate(content.encode("utf-8"))[0]
    # Return the pure stdout
    return stdout
