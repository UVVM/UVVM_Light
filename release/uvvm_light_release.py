import subprocess
import os
import glob
import sys
from shutil import copyfile
from datetime import date

try:
    from hdlregression import HDLRegression
except:
    print('Unable to import HDLRegression module. See HDLRegression documentation for installation instructions.')
    sys.exit(1)

uvvm_github = "git@github.com:UVVM/UVVM.git"


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


'''
Clone UVVM repo - UVVM Light will be created from source.
'''
def prepare_internal_repo(current_dir):
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


'''
Create a list of all the files to copy to UVVM light
'''
def locate_files_to_copy():
    print('Locating UVVM Util src files.')
    files_to_copy = [filename for filename in glob.glob("./uvvm/uvvm_util/src/*.vhd")]
    print('Locating UVVM Util doc files.')
    files_to_copy += [filename for filename in glob.glob("./uvvm/uvvm_util/doc/*.pdf")]
    files_to_copy += [filename for filename in glob.glob("./uvvm/uvvm_util/doc/*.pps")]
    print('Locating BFM src files.')
    files_to_copy += [filename for filename in glob.glob("./uvvm/bitvis_*/src/*bfm*.vhd")]
    print('Locating RST/HTML files.')
    files_to_copy += [filename for filename in glob.glob("./uvvm/doc/**/*.*", recursive=True)]

    return files_to_copy


'''
Print the list of files
'''
def present_files(files_to_copy):
    print(" - Files found: %i." % (len(files_to_copy)))
    for idx, item in enumerate(files_to_copy):
        print("(%i) --> %s" % (idx, item))


'''
Replace all the local files with the list of files
'''
def copy_files(files_to_copy, current_dir):
    print("Delete local files before copying new files")
    execute_and_print(["rm", "-r", "../src_bfm/*.vhd"])
    execute_and_print(["rm", "-r", "../src_util/*.vhd"])
    execute_and_print(["rm", "-r", "../doc/*"])

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


'''
Compile all files and simulate demo tb
'''
def test_compilation(current_dir):
    if os.path.isdir("hdlregression"):
        print("Clean old simulation files")
        execute_and_print(["rm", "-r", "hdlregression"])

    hr = HDLRegression()

    # Add util files
    hr.add_files("../src_util/*.vhd", "uvvm_util")
    # Add BFM files
    hr.add_files("../src_bfm/*.vhd", "work")
    # Add DUT files
    hr.add_files("../demo_tb/dut/*.vhd", "work")
    # Add TB files
    hr.add_files("../demo_tb/*.vhd", "work")

    hr.start()

    # Exit if demo TB wasn't run or it had errors
    num_passing_tests = hr.get_num_pass_tests()
    num_failing_tests = hr.get_num_fail_tests()
    if num_passing_tests == 0 or num_failing_tests != 0:
        print(" - aborting")
        sys.exit(1)

    # Verify scripts
    print('\nVerify compile.sh script...')
    (ret_txt, ret_code) = hr.run_command(["sh", "../script/compile.sh"], False)
    if ret_code != 0:
        print(ret_txt)
        print(" - aborting")
        sys.exit(1)
    print('\nVerify compile_and_run_demo_tb.do script...')
    (ret_txt, ret_code) = hr.run_command(["vsim", "-c", "-do", "do ../sim/compile_and_run_demo_tb.do; exit"], False)
    if ret_code != 0:
        print(ret_txt)
        print(" - aborting")
        sys.exit(1)


'''
Delete simulation files.
'''
def cleanup():
    print(" - removing simulation files")
    execute_and_print(["rm", "-r", "hdlregression"])
    execute_and_print(["rm", "modelsim.ini"])
    execute_and_print(["rm", "transcript"])
    execute_and_print(["rm", "*.txt"])
    execute_and_print(["rm", "*.cf"])
    execute_and_print(["rm", "-r", "uvvm_util"])
    execute_and_print(["rm", "-r", "../sim/uvvm_util"])


'''
Publish release changes to GitHub.
'''
def publish_github(commit_msg : str = None):
    print("""\n
    Preparing for publishing of changes to UVVM_Light:
    ----------------------------------------------------
    1. Setting up git user
    2. Adding all changes and committing
    3. Pushing to GitHub UVVM_Light master branch
    4. Returning to GitHub master branch for clean-up
    \n
    """)

    if commit_msg is None:
      date_tag = date.today().strftime("%Y.%m.%d")
      commit_msg = 'Updated to UVVM Light version v2 %s - Please see CHANGES.txt for details.' % (date_tag)

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

    print("Adding files and committing")
    execute_and_print(["git", "add", "../src_bfm/."])
    execute_and_print(["git", "add", "../src_util/."])
    execute_and_print(["git", "add", "../doc/."])
    execute_and_print(["git", "add", "../script/."])
    execute_and_print(["git", "add", "../release/."])
    execute_and_print(["git", "add", "../demo_tb/."])

    execute_and_print(["git", "add", "-u"])
    execute_and_print(["git", "clean", "-fdx"])
    execute_and_print(["git", "commit", "-m", commit_msg], allow_fail=True)

    print("On UVVM Light master branch: pushing to GitHub UVVM_Light repository, master branch")
    execute_and_print(["git", "push", "uvvm_light_remote"])
    execute_and_print(["git", "push", "uvvm_light_backup_remote"])


'''
Find the latest UVVM version.
'''
def find_uvvm_version(filename):
    with open(filename, 'r', encoding="utf-8") as in_file:
        for line in in_file:
            if "C_UVVM_VERSION" in line:
                parts = line.split("\"")
                return parts[1]
    print("UVVM version not found - aborting")
    sys.exit(1)


def main():
    current_dir = os.getcwd()
    uvvm_version_file = "../src_util/methods_pkg.vhd"

    print("\nNote! This program will clone UVVM repository and update all src files on UVVM_Light repository.")
    print("If a mismatch in file numbers occurs, the script will end.")
    print("After copy, the script will compile all BFM src files and run the demo TB.")
    print("After compile and simulation the script will remove any generated files and push to GitHub.\n%s" % (80*'='))

    print('\nFetching UVVM repository and checking out master branch.')
    prepare_internal_repo(current_dir)

    print("%s\nCreating list of all UVVM light files available:" % (80*'='))
    files_to_copy = locate_files_to_copy()
    present_files(files_to_copy)
    copy_files(files_to_copy, current_dir)

    print("\nTesting compilation and demo TB.")
    test_compilation(current_dir)

    print("\nCleaning up repository.")
    cleanup()

    print("\nPublishing release changes to GitHub")
    publish_github("Updated to UVVM Light version " + find_uvvm_version(uvvm_version_file) + " - Please see CHANGES.TXT for details.")

    print("==========================================================================")
    print(" UVVM_Light RELEASE DONE\n")


if __name__ == "__main__":
    main()
