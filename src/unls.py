#!/usr/bin/env python3
# vi: ft=python
# <!-- Imports -->
from typing import Union, List
from os import getenv
from sys import platform
from subprocess import run
from log import debug, info, warn, error
from gpg import GPG_CMD, decrypt_file
from utils import check_deps
from engine import connect
# <!-- Code -->
# LINUX
HOME: str = getenv("HOME", "") if platform == "linux" else ""


# <!-- Main -->
if __name__ == "__main__":
    warn("This program is still in development! Contact the developers if any issues arise.")
    # <!-- Get environment variables -->
    uni_fldr: Union[str, None] = getenv("UNI_FLDR")
    if uni_fldr is None:
        error("University folder environment variable must be set!", 1)
    else:
        debug(f"Set university folder as '{uni_fldr}'")
        uni_fldr = uni_fldr.replace("~", HOME)

    # <!-- Check dependencies -->
    check_deps([
        GPG_CMD, "nmcli", "geckodriver"
    ])
    # <!-- Verify SSIDs -->
    info("Verifying SSIDs...")
    # Read accepted ssids file
    connected_networks: List[str] = run(
        ["nmcli", "-t", "-f", "NAME", "c", "s", "-a"],
        capture_output=True, text=True
    ).stdout.split()
    with open(f"{uni_fldr}/accepted_ssids", "r") as file:
        accepted_networks: List[str] = file.read().split()
    # Check if current network is accepted
    verified: Union[str, bool] = False
    for network in connected_networks:
        if network in accepted_networks:
            verified = network
    # Exit if not verified, else debug
    if not verified:
        error("None of the connected networks are allowed to login -- Exiting!", 1)
    else:
        debug(f"Network '{verified}' is accepted, continuing!")

    # <!-- Verify credentials -->
    info("Getting user credentials...")
    # Get username and password
    uni_user: str = decrypt_file(f"{uni_fldr}/cred/username", None)
    uni_pass: str = decrypt_file(f"{uni_fldr}/cred/password", None)

    with open(f"{uni_fldr}/login_url", "r") as file:
        url: str = file.read().strip()
    # <!-- Login -->
    connect(url, {
        "username": uni_user,
        "password": uni_pass,
    })
    # <!-- Finish -->
    info("Done!")
