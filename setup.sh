#/bin/bash
set -ex
pwd=$(cd $(dirname $0); pwd)

cd "$pwd/pwndbg"
PWNDBG_VENV_PATH="$pwd/.venv" ./setup.sh

cd $pwd
.venv/bin/pip install -e .

echo "source $pwd/gdbinit.py" > $HOME/.gdbinit
echo "source $pwd/pwndbg/gdbinit.py" >> $HOME/.gdbinit
echo "source $pwd/postinit.py" >> $HOME/.gdbinit
