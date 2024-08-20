import subprocess
import os
import glob
import sys
import platform
from shutil import copyfile
from pprint import pprint
from datetime import date
# from builtins import

uvvm_github = "git@github.com:UVVM/UVVM.git"


def prepare_internal_repo(current_dir):
    '''
    Clone UVVM repo - UVVM Light will be created from source.
    '''
    if os.path.isdir("uvvm"):
        print(" - Updating UVVM repository")
        os.chdir("uvvm")
        process = subprocess.Popen(
            ["git", "pull", uvvm_github], stdout=subprocess.PIPE)
        process.wait()
    else:
        print(" - Cloning UVVM from GitHub")
        process = subprocess.Popen(
            ["git", "clone", uvvm_github], stdout=subprocess.PIPE)
        process.wait()
        os.chdir("uvvm")

    print(" - Ensure UVVM is on master branch.")
    process = subprocess.Popen(
        ["git", "checkout", "master"], stdout=subprocess.PIPE)
    process.wait()
    os.chdir(current_dir)


def execute(cmd, allow_fail=False):
    popen = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code and allow_fail is False:
        raise subprocess.CalledProcessError(return_code, cmd)


def execute_and_print(cmd, allow_fail=False):
    for path in execute(cmd, allow_fail):
        print(path, end="")


def cleanup():
    '''
    Delete cloned repository and simualtion files.
    '''
    print(" - removing simulation files")
    execute_and_print(["rm", "modelsim.ini"])
    execute_and_print(["rm", "transcript"])
    execute_and_print(["rm", "*.txt"])
    execute_and_print(["rm", "-r", "uvvm_util"])
    # execute_and_print(["rm", "../sim/*.txt"])
    # execute_and_print(["rm", "../sim/modelsim.ini"])
    # execute_and_print(["rm", "../sim/transcript"])
    # execute_and_print(["rm", "-r", "../sim/uvvm_util"])


def copy_files(files_to_copy, current_dir):
    for item in files_to_copy:
        filename = os.path.basename(item)
        filename_with_path = os.path.abspath(item)

        if '.vhd' in filename.lower():
            if 'uvvm_util' not in filename_with_path.lower():
                # if 'bfm' in filename.lower() and 'bfm_common_pkg' not in filename.lower():
                target_name = os.path.join(
                    current_dir, '../src_bfm/', filename)
                print('[COPY SRC_BFM] %s --> %s' % (item, target_name))
            else:
                target_name = os.path.join(
                    current_dir, '../src_util/', filename)
                print('[COPY SRC_UTIL] %s --> %s' % (item, target_name))
        else:

            if 'build' in filename_with_path.lower() or 'source' in filename_with_path.lower():

                filename_with_path = filename_with_path.replace('\\', '/')
                filename_with_path = filename_with_path.replace('uvvm/', '../')

                target_name = os.path.join(
                    current_dir, '../doc/', filename_with_path)
                print('[COPY DOC RST] %s --> %s' % (item, target_name))

                path = os.path.dirname(target_name)
                os.makedirs(path, exist_ok=True)

            else:
                target_name = os.path.join(current_dir, '../doc/', filename)
                print('[COPY DOC] %s --> %s' % (item, target_name))

        copyfile(item, target_name)


def locate_files_to_copy():
    print('Locating UVVM Util src files.')
    files_to_copy = [filename for filename in glob.glob(
        "./uvvm/uvvm_util/src/*.vhd")]
    print('Locating UVVM Util doc files.')
    files_to_copy += [filename for filename in glob.glob(
        "./uvvm/uvvm_util/doc/*.pdf")]
    files_to_copy += [filename for filename in glob.glob(
        "./uvvm/uvvm_util/doc/*.html")]
    files_to_copy += [filename for filename in glob.glob(
        "./uvvm/uvvm_util/doc/*.pps")]

    print('Locating BFM src files.')
    files_to_copy += [filename for filename in glob.glob(
        "./uvvm/bitvis_*/doc/*bfm*.pdf")]
    files_to_copy += [filename for filename in glob.glob(
        "./uvvm/bitvis_*/doc/*bfm*.html")]
    files_to_copy += [filename for filename in glob.glob(
        "./uvvm/bitvis_*/src/*bfm*.vhd")]

    print('Locating RST/HTML files.')
    files_to_copy += [filename for filename in glob.glob(
        "./uvvm/doc/**/*.*", recursive=True)]

    return files_to_copy


def present_files(files_to_copy):
    print(" - Files found: %i." % (len(files_to_copy)))
    for idx, item in enumerate(files_to_copy):
        print("(%i) --> %s" % (idx, item))


def test_compilation(current_dir):
    print(" - Compiling uvvm_util files.")
    execute_and_print(["vlib", "uvvm_util"])
    execute_and_print(["vmap", "work", "uvvm_util"])
    execute_and_print(
        ["vsim", "-c", "-do", "../script/compile.do", "-do", "exit"])

    ok = input(" - Compilation ok [Y/N] ?")
    if ok.lower() == 'y':
        print(" - Compiling and running demo tb.")
        execute_and_print(
            ["vsim", "-c", "-do", "../sim/compile_and_run_demo_tb.do", "-do", "exit"])
        os.chdir(current_dir)
    else:
        print(" - aborting")
        sys.exit(1)

    ok = input(" - Simuations ok [Y/N] ?")
    if ok.lower() != 'y':
        print(" - aborting")
        sys.exit(1)


def publish_github(commit_msg : str = None):
    print("""\n
    Preparing for publishing of changes to UVVM_Light:
    ----------------------------------------------------
    1. Setting up git user
    2. Adding all changes and commiting
    3. Pushin to GitHub UVVM_Light master branch
    4. Returning to gitlab master branch for clean-up
    \n
    """)

    
    
    if commit_msg is None:
      date_tag = date.today().strftime("%y.%m.%d")
      commit_msg = '"Updated to UVVM v%s"' % (date_tag)

    print("Setting up remote GitHub UVVM Light")
    uvvm_light_remote = "git remote add uvvm_light_remote git@github.com:UVVM/UVVM_Light.git"
    uvvm_light_backup_remote = "git remote add uvvm_light_backup_remote git@github.com:UVVM/UVVM_Light_internal.git"

    execute_and_print(uvvm_light_remote, allow_fail=True)
    execute_and_print(uvvm_light_backup_remote, allow_fail=True)

    print("Setting up UVVM as Git user")
    execute_and_print(["git", "config", "user.name", "UVVM"])
    execute_and_print(["git", "config", "user.email", "info@bitvis.no"])

    print("Deleting cloned repository uvvm")
    os.system("rm -rf uvvm")

    print("Adding files and commiting")
    execute_and_print(["git", "add", "../src_bfm/."])
    execute_and_print(["git", "add", "../src_util/."])
    execute_and_print(["git", "add", "../doc/."])
    execute_and_print(["git", "add", "../script/."])
    execute_and_print(["git", "add", "../release/."])
    execute_and_print(["git", "add", "../demo_tb/."])

    execute_and_print(["git", "add", "-u"])
    execute_and_print(["git", "clean", "-fdx"])
    execute_and_print(["git", "commit", "-m", commit_msg], allow_fail=True)

    #execute_and_print(["git", "branch", "-M", "main"])
    #execute_and_print(["git", "checkout", "main"])

    print("On UVVM Light master branch: pushing to GitHub UVVM_Light repositoty, master branch")
    execute_and_print(["git", "push", "uvvm_light_remote"])
    execute_and_print(["git", "push", "uvvm_light_backup_remote"])


def main():
    current_dir = os.getcwd()

    print("\nNote! This program will clone UVVM repository and update all src files on UVVM_Light repository.")
    print("If a mismatch in file numbers occure, the script will end.")
    print("After copy, the script will compile all BFM src files and run the demo TB.")
    print("After compile and simulation the script will remove any generated files and push to GitHub.\n%s" % (80*'='))

    print('\nFetching UVVM reposity and checking out master branch.')
    prepare_internal_repo(current_dir)

    print("%s\nCreating list of all util vhd files available:" % (80*'='))

    files_to_copy = locate_files_to_copy()
    present_files(files_to_copy)
    copy_files(files_to_copy, current_dir)

    print("\nTesting compilation and demo TB.")
    test_compilation(current_dir)

    print("\nCleaning up repository.")
    cleanup()

    print("\nPublishing release changes to GitHub")
    publish_github()

    print("==========================================================================")
    print(" UVVM_Light RELEASE DONE\n")


if __name__ == "__main__":
    main()
