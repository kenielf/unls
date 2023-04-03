from typing import List
from subprocess import run, DEVNULL
from log import debug, error


#CMDS="nmcli gpg"
#for prog in ${CMDS}; do
#    command -v "${prog}" >/dev/null 2>&1 && \
#        echo -e "\x1b[32m[EXISTS]\x1b[00m ${prog}" || \
#        echo -e "\x1b[31m[DOES NOT EXIST]\x1b[00m ${prog}"
#done
def check_deps(dep_list: List[str]) -> None:
    missing: List[str] = []
    for program in dep_list:
        code: int = run(["which", program], stdout=DEVNULL, stderr=DEVNULL).returncode
        if code != 0:
            missing.append(program)
            error(f"Could not find '{program}'")
        else:
            debug(f"Found '{program}'")
    if len(missing) != 0:
        error("There were missing applications, exiting!", 1)

