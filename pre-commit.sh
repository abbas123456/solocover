# pre-commit.sh

# Run the gauntlet...

# stash uncommitted changes
git stash -q --keep-index

# run unit tests
fab test
UNIT_TESTS_RESULT=$?
[ $UNIT_TESTS_RESULT -ne 0 ] && exit 1

# run acceptance tests
#./manage.py harvest --settings=settings_test -v 2
#ACCEPTANCE_TESTS_RESULT=$?
#[ $ACCEPTANCE_TESTS_RESULT -ne 0 ] && git stash pop -q; exit 1

# find console.log in js code
#FILES_PATTERN='\.(js|coffee)(\..+)?$'
#FORBIDDEN='console.log'
#git diff --cached --name-only | \
    #grep -E $FILES_PATTERN | \
    #GREP_COLOR='4;5;37;41' xargs grep --color --with-filename -n $FORBIDDEN
#JS_DEBUGGING_TEST=$?

#if [[ $JS_DEBUGGING_TEST -ne 0 ]]; then
    #echo "COMMIT REJECTED Found $FORBIDDEN references. Please remove them before commiting";
    #git stash pop -q;
    #exit 1
#fi

# find ipdb.set_trace() in python code
#FILES_PATTERN='\.py(\..+)?$'
#FORBIDDEN='ipdb\.set_trace\(\)'
#git diff --cached --name-only | \
    #grep -E $FILES_PATTERN | \
    #GREP_COLOR='4;5;37;41' xargs grep --color --with-filename -n $FORBIDDEN
#PY_DEBUGGING_TEST=$?
#if [[ $PY_DEBUGGING_TEST -ne 0 ]]; then
    #echo "COMMIT REJECTED Found $FORBIDDEN references. Please remove them before commiting";
    #git stash pop -q;
    #exit 1
#fi

# run pep8 against codebase
FILES=$(git diff --cached --name-status | grep -v ^D | awk '$1 $2 { print $2}' | grep -e .py$)
if [ -n "$FILES" ]; then
    pep8 $FILES
    PEP8_RESULT=$?
    git stash pop -q
    [ $PEP8_RESULT -ne 0 ] && exit 1
fi

# run pyflakes against codebase
#pyflakes .
#PYFLAKES_RESULT=$?
#[ $PYFLAKES_RESULT -ne 0 ] && git stash pop -q; exit 1

#run jshint against codebase
#jshint www/static/js/
#JSHINT_RESULT=$?
#[ $JSHINT_RESULT -ne 0 ] && git stash pop -q; exit 1

exit 0
