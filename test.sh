#!/bin/bash -e

BIN="$PWD/$1"
SRC="$PWD/$2"
OUT="$(mktemp)"

cd "$(dirname "$0")"

HARNESS="py/test*.py py/util.py"

function submit() {
    echo -e  '\033[36;1m============================================================'
    echo -e  '                           Finish                           '
    echo -e  '============================================================\033[0m'

    echo -e '\n------------------------------------------------------------\n\n' >> $OUT
    cat $SRC >> $OUT

    if [[ $PASSED == 1 ]]; then
        echo -e "\033[32;1m"
        echo '                                                                   *'
        echo '                                                    +'
        echo '                                          +    +'
        echo '                                   +     +'
        echo '                              +      +'
        echo '   + + + + +              +     +'
        echo '     +        +       +     +'
        echo '        +       + +      +'
        echo '           +   +      +'
        echo '             +      + +'
        echo '         +      +        +'
        echo '      +       +    +        +'
        echo '    +       +         +        +'
        echo '   + + + + +             + + + + +'
        echo
        echo '   _____ _    _  _____ _____ ______  _____ _____ '
        echo '  / ____| |  | |/ ____/ ____|  ____|/ ____/ ____|'
        echo ' | (___ | |  | | |   | |    | |__  | (___| (___  '
        echo '  \___ \| |  | | |   | |    |  __|  \___ \\___ \ '
        echo '  ____) | |__| | |___| |____| |____ ____) |___) |'
        echo ' |_____/ \____/ \_____\_____|______|_____/_____/ '
        echo
        echo -e "\033[0m"
    else
        echo -e "\033[31;1mFAIL\033[0m: Some tests failed.\n\n"
        exit 1
    fi
}

trap submit EXIT

for TEST in test/*.txt; do
    echo -e "\033[36;1m============================================================"
    echo -e "$TEST"
    echo -e "============================================================\033[0m"
    $BIN $OUT $TEST
done
PASSED=1
