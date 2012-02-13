import os
import virtualenv, textwrap

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

output = virtualenv.create_bootstrap_script(textwrap.dedent("""
import os, subprocess, sys

sys.argv.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

def extend_parser(parser):
    # parser.set_default('no_site_packages', True)
    parser.set_default('clear', True)

def after_install(options, home_dir):
    # Make a copy of the pristine zc.buildout
    print "Installing zc.buildout"
    if sys.platform == 'win32':
        bin_dir = join(home_dir, 'Scripts')
        subprocess.call([os.path.join(bin_dir, 'python'), os.path.join(bin_dir, 'easy_install-script.py'), 'zc.buildout'])
    else:
        bin_dir = join(home_dir, 'bin')
        subprocess.call([os.path.join(bin_dir, 'easy_install'), 'zc.buildout'])
"""))

f = open(os.path.join(PROJECT_DIR, 'bin', 'bootstrap.py'), 'w')
try:
    f.write(output)
finally:
    f.close()