if [ `command -v ipython` ]; then
    CMD=ipython
else
    CMD=python
fi

$CMD -i shell.py
