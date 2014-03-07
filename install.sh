#!/bin/bash

PREFIX=/usr/local

INSTALLDIR="$PREFIX/share/tomate"
BINDIR="$PREFIX/bin"

# Are we root?
if [ $EUID -ne 0 ]; then
    echo "Você precisa ser root para rodar este escript." 2>&1
    exit 1
else
    # onde está o python 2?
    if [ ! $(which python2 >/dev/null 2>&1) ]; then
        sed -i "1 s;python2;python;" tomate.py
    fi
    mkdir -p "$INSTALLDIR"
    cp *.{png,svg,py} "$INSTALLDIR/"
    rm -f "$BINDIR/tomate"
    ln -s "$INSTALLDIR/tomate.py" "$BINDIR/tomate"
fi
