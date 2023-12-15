from __future__ import annotations

import glob
import os
import site
import sys
from glob import glob
from os import path

SKIP_CONST = "PWNDBG_PLEASE_SKIP_VENV"
venv_path = os.environ.get("PWNDBG_VENV_PATH")
if venv_path == SKIP_CONST or path.exists(path.dirname(__file__) + "/.skip-venv"):
  pass
else:
  directory = path.split(__file__)[0]
  directory = path.expanduser(directory)
  directory = path.abspath(directory)

  if not venv_path:
    venv_path = os.path.join(directory, ".venv")

  if not os.path.exists(venv_path):
    print(f"Cannot find Pwndbg virtualenv directory: {venv_path}: please re-run setup.sh")
    sys.exit(1)

  site_pkgs_path = glob(os.path.join(venv_path, "lib/*/site-packages"))[0]

  # add virtualenv's site-packages to sys.path and run .pth files
  site.addsitedir(site_pkgs_path)

  # remove existing, system-level site-packages from sys.path
  for site_packages in site.getsitepackages():
    if site_packages in sys.path:
      sys.path.remove(site_packages)

  # Set virtualenv's bin path (needed for utility tools like ropper, pwntools etc)
  bin_path = os.path.join(venv_path, "bin")
  os.environ["PATH"] = bin_path + os.pathsep + os.environ.get("PATH")

  # Add pwndbg directory to sys.path so it can be imported
  sys.path.insert(0, directory)

  # Push virtualenv's site-packages to the front
  sys.path.remove(site_pkgs_path)
  sys.path.insert(1, site_pkgs_path)

  # skip venv initialization in pwndbg
  os.environ["PWNDBG_VENV_PATH"] = SKIP_CONST

os.environ["PWNLIB_NOTERM"] = "1"

from pwndbgex import load

load()
