#!/usr/bin/env python
__author__ = 'johann'

import os
import subprocess
import fileinput
import shutil

from sys import stderr
from sys import stdin
from sys import stdout
from sys import argv

import random
random = random.SystemRandom()

TERMINAL_WIDTH = 80 

venv_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'venv/bin')


def get_executable_path(executable):
    if len(argv) > 1 and argv[1] == '--venv':
        print os.path.join(venv_path, executable)
        return os.path.join(venv_path, executable)
    return executable


def get_random_string(length=12,
                      allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    """
    Returns a securely generated random string.

    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits.

    Taken from the django.utils.crypto module.
    """
    return ''.join(random.choice(allowed_chars) for i in range(length))


def get_secret_key():
    """
    Create a random secret key.

    Taken from the Django project.
    """
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return get_random_string(50, chars)


def get_answer(question, proper_answers=('yes','no')):
    """
    Ask a question and keep asking until a proper answer is received.

    Default proper answers are 'yes' and 'no'.
    """
    answer = ''
    while answer not in proper_answers:
        stdout.write(question)
        stdout.flush()
        answer = stdin.readline().strip().lower()
    return answer


print "*" * TERMINAL_WIDTH
print "Setting up Wasa2il from scratch with an SQLite database called 'wasa2il.sqlite'."
print "This script assumes that both Python and Pip are installed."
print "*" * TERMINAL_WIDTH


# Install (or upgrade) Python package dependencies
stdout.write('Installing dependencies:\n')
result = subprocess.call([get_executable_path("pip"), "install", "--upgrade", "-r", "requirements.txt"])
if result == 0:
    stdout.write('Dependency installation complete.\n')
else:
    if get_answer('Dependency installation seems to have failed. Continue anyway? (yes/no): ') != 'yes':
        stdout.write('Okay, quitting.\n')
        quit(1)


# Check if Django is installed
try:
    stdout.write('Checking if Django is installed...')
    stdout.flush()
    import django
    stdout.write(' yes (%d.%d.%d)\n' % (django.VERSION[0], django.VERSION[1], django.VERSION[2]))
except ImportError:
    stdout.write(' no\n')
    stderr.write('Error: Cannot continue without Django which should be installed but is not. Quitting.\n')
    quit(2)


# Check if local_settings.py exists and create it if it doesn't
setup_local_settings = False
if not os.path.exists('wasa2il/local_settings.py'):
    # Create the file from local_settings.py-example
    stdout.write('Creating local settings file (local_settings.py)...')
    stdout.flush()
    try:
        shutil.copy('wasa2il/local_settings.py-example', 'wasa2il/local_settings.py')
        stdout.write(' done\n')
    except IOError as e:
        stdout.write(' failed\n')
        stderr.write('%s\n' % e.__str__())
        quit(1)


# Go through local_settings.py and fix settings if needed
stdout.write('Checking local settings configuration:\n')
local_settings_changed = False
for line in fileinput.input('wasa2il/local_settings.py', inplace=1):
    if line.startswith("SECRET_KEY = ''"):
        stdout.write('- Setting secret key to random string...')
        stdout.flush()
        print "SECRET_KEY = '%s'" % get_secret_key()
        stdout.write(' done\n')
        local_settings_changed = True
    elif line.startswith("DATABASE_ENGINE = 'django.db.backends.'"):
        stdout.write('- Configuring database engine (SQLite)...')
        stdout.flush()
        print "DATABASE_ENGINE = 'django.db.backends.sqlite3'"
        stdout.write(' done\n')
        local_settings_changed = True
    elif line.startswith("DATABASE_NAME = ''"):
        stdout.write('- Setting database name (wasa2il.sqlite)...')
        stdout.flush()
        print "DATABASE_NAME = 'wasa2il.sqlite'"
        stdout.write(' done\n')
        local_settings_changed = True
    else:
        print line.strip()

if not local_settings_changed:
    stdout.write('- No changes needed.\n')


# Change to Wasa2il's directory
os.chdir('wasa2il')


# Compile the translation files
for lang in next(os.walk(os.path.join(os.getcwd(), 'locale')))[1]:
    print [get_executable_path('pybabel'), 'compile', '-d', os.path.join(os.getcwd(), 'locale'), '-D', 'django', '-l', lang]
    subprocess.call([get_executable_path('pybabel'), 'compile', '-d', os.path.join(os.getcwd(), 'locale'), '-D', 'django', '-l', lang])


# Setup database if needed
create_database = False
if os.path.exists('wasa2il.sqlite'):
    if get_answer('SQLite database already exists. Kill it and start over? (yes/no): ') == 'yes':
        stdout.write('Deleting wasa2il.sqlite...')
        stdout.flush()
        os.remove('wasa2il.sqlite')
        stdout.write(' done\n')
        create_database = True
else:
    create_database = True

if create_database:
    stdout.write('Setting up database (via "migrate"):\n')
    migrate_result = subprocess.call([get_executable_path('python'), os.path.join(os.getcwd(), 'manage.py'), 'migrate'])

    if migrate_result != 0:
        stderr.write('Error: Django migration gave errors. Quitting.\n')
        quit(1)

    stdout.write('We will now create a superuser to configure polities within Wasa2il once it has been set up.\n')
    subprocess.call([get_executable_path('python'), os.path.join(os.getcwd(), 'manage.py'), 'createsuperuser'])


print "*" * TERMINAL_WIDTH
print "All done!"
print "To run Wasa2il and start configuring polities, follow these steps:"
print "- Go to the 'wasa2il' directory and run 'python manage.py runserver'"
print "- Open your favorite browser and type in: http://localhost:8000"
print "- Log in with the superuser account created previously"
print
print "(If you don't have a superuser account yet, then go to the 'wasa2il' directory"
print "and run 'python manage.py createsuperuser')"
print "*" * TERMINAL_WIDTH


