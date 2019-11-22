import subprocess, os, glob, sys, platform
from shutil import copyfile
from pprint import pprint
from datetime import date

uvvm_stash = "ssh://git@stash.bitvis.no/bv_uvvm/uvvm_public.git"
current_dir = os.getcwd()
uvvm_internal_list = []
uvvm_light_list =[] 
os_is_windows = False

def set_os():
    global os_is_windows
    if 'windows' in platform.system().lower():
        os_is_windows = True
    else:
        os_is_windows = False


def prepare_internal_repo():
    global current_dir

    if os.path.isdir("uvvm_public"):
        print(" - Updating uvvm_public repository")
        os.chdir("uvvm_public")
        process = subprocess.Popen(["git", "pull", uvvm_stash], stdout=subprocess.PIPE)
        process.wait()
    else:
        print(" - Cloning UVVM from Stash")
        process = subprocess.Popen(["git", "clone", uvvm_stash], stdout=subprocess.PIPE)
        process.wait()
        os.chdir("uvvm_public")

    print(" - Ensure barnch is master")
    process = subprocess.Popen(["git", "checkout", "master"], stdout=subprocess.PIPE)
    process.wait()
    os.chdir(current_dir)

def cleanup(repo):
    print(os.getcwd())
    print(" - removing directory /uvvm_public")
    #subprocess.call(["rm", "-r", "-f", repo], stderr=subprocess.PIPE)
    print(" - removing simulation files")
    subprocess.call(["rm", "modelsim.ini"], stderr=subprocess.PIPE)
    subprocess.call(["rm", "transcript"], stderr=subprocess.PIPE)
    subprocess.call(["rm", "-r", "uvvm_util"], stderr=subprocess.PIPE)
    subprocess.call(["rm", "sim/*.txt"], stderr=subprocess.PIPE)
    subprocess.call(["rm", "sim/modelsim.ini"], stderr=subprocess.PIPE)
    subprocess.call(["rm", "sim/transcript"], stderr=subprocess.PIPE)
    subprocess.call(["rm", "-r", "sim/uvvm_util"], stderr=subprocess.PIPE)


def copy_files(src_list, target_list):
    for idx in range(0, len(src_list)-1):
        print(" - Copy: %s ---->> %s" %(src_list[idx], target_list[idx]))
        copyfile(src_list[idx], target_list[idx])
        


def get_bfm_files(path):
    bfm_files = [f for f in glob.glob(path + "/**/*bfm*[!tb].vhd", recursive=True)]
    return bfm_files

def save_in_copy_files(index, items):
    global copy_files
    for item in items:
        copy_files[index].append(item)


def remove_not_listed(target, src):
    src_copy = []
    target_copy = []

    # Get BFM file names only (no path)
    for idx, item in enumerate(src):
        if os_is_windows:
            src_copy.append(item[item.rfind('\\')+1:])
        else:
            src_copy.append(item[item.rfind('/')+1:])

    # Search and keep
    for idx in range(0, len(target)):

        # Get BFM file names only (no path)
        if os_is_windows:
            search_item = target[idx][target[idx].rfind('\\')+1:]
        else:
            search_item = target[idx][target[idx].rfind('/')+1:]

        # Store        
        if search_item in src_copy:
            target_copy.append(target[idx])

    return target_copy



def add_to_list(target_list, src_list):
    for item in src_list:
        target_list.append(item)
 

def show_error(src_list, target_list):
    print("Src %i:" %(len(src_list)))
    for item in src_list:
        print(item)

    print("\nTarget %i:" %(len(target_list)))
    for item in target_list:
        print(item)


def present_files(src_list, target_list):
    print(" - File numbers: src=%i, target=%i." %(len(src_list), len(target_list)))

    if len(src_list) != len(target_list):
        print("ERROR! Missing files!")
        show_error(src_list, target_list)
        sys.exit(1)

    for idx in range(0, len(src_list)):
        print(" - " + src_list[idx] + "   << ---- >>   " + target_list[idx])




def test_compilation():
    global current_dir
    
    print(" - Compiling uvvm_util files.")
    subprocess.call(["vlib", "uvvm_util"], stderr=subprocess.PIPE)
    subprocess.call(["vmap", "work", "uvvm_util"], stderr=subprocess.PIPE)
    subprocess.call(["vsim", "-c", "-do", "compile.do", "-do", "exit"], stderr=subprocess.PIPE)

    ok = input(" - Compilation ok [Y/N] ?")
    if ok.lower() == 'y':
        print(" - Compiling and running demo tb.")
        os.chdir("sim")
        subprocess.call(["vsim", "-c", "-do", "compile_and_run_demo_tb.do", "-do", "exit"], stderr=subprocess.PIPE)
        os.chdir(current_dir)
    else:
        print(" - aborting")
        sys.exit(1)

    ok = input(" - Simuations ok [Y/N] ?")
    if ok.lower() == 'n':
        print(" - aborting")
        sys.exit(1)




def publish_github():
    github_remote = "git remote add github  git@github.com:UVVM/UVVM_Light.git"
    stash_remote = "git remote add public ssh://git@stash.bitvis.no/bv_uvvm/uvvm_light.git"
    #date_tag = date.today().strftime("%y.%m.%d")
    date_tag = "19.11.21"
    commit_msg = '"Updated to UVVM v20' + date_tag + '"' 

    print("Setting up remotes (Stash and GitHub)")
    subprocess.call(stash_remote, stderr=subprocess.PIPE)
    subprocess.call(github_remote, stderr=subprocess.PIPE)

    print("Setting up UVVM as Git user")
    subprocess.call(["git", "config", "user.name", "UVVM"], stderr=subprocess.PIPE)
    subprocess.call(["git", "config", "user.email", "info@bitvis.no"], stderr=subprocess.PIPE)

    print("On branch master: adding all changes, commit and push to Stash master branch")
    subprocess.call(["git", "add", "-u"], stderr=subprocess.PIPE)
    subprocess.call(["git", "clean", "-fdx"], stderr=subprocess.PIPE)
    subprocess.call(["git", "commit", "-m", commit_msg], stderr=subprocess.PIPE)
    subprocess.call(["git", "push", "origin", "master"], stderr=subprocess.PIPE)

    print("On master branch: check out public branch")
    subprocess.call(["git", "checkout", "public"], stderr=subprocess.PIPE)

    print("On public branch: adding files, commit and push to Stash public branch")
    subprocess.call(["git", "add", "-u"], stderr=subprocess.PIPE)
    subprocess.call(["git", "clean", "-fdx"], stderr=subprocess.PIPE)

    subprocess.call(["git", "commit", "-m", commit_msg], stderr=subprocess.PIPE)
    subprocess.call(["git", "push", "origin", "public"], stderr=subprocess.PIPE)

    print("On public branch: pushing to GitHub UVVM_Light repositoty, master branch")
    subprocess.call(["git", "push", "github", "master"], stderr=subprocess.PIPE)


    print("On public branch: check out master branch")
    subprocess.call(["git", "checkout", "master"], stderr=subprocess.PIPE)



def main():
    print("\nNote! This program will clone UVVM_Public repository and update all src files on UVVM_Light branch")
    print("with the content from UVVM_Public branch.")
    print("If a mismatch in file numbers occure, the script will end.")
    print("After copy, the script will compile all BFM src files and run the demo TB.")
    print("After compile and simulation the script will remove any generated files and push to GitHub and Stash.\n")


    set_os()

    print('Fetching UVVM_public reposity and checking out master branch.')
    prepare_internal_repo()

    print("Creating list of all util vhd files available:")


    print("\nSearching for Util VHD files. ", end='')
    util_vhd_files_src = [f for f in glob.glob("./uvvm_public/uvvm_util/src/*.vhd")]
    util_vhd_files_target = [item.replace("uvvm_public/uvvm_util/src", "src_util") for item in util_vhd_files_src]
    print("Found: src=%i, target=%i." %(len(util_vhd_files_src), len(util_vhd_files_target)))

    add_to_list(uvvm_internal_list, util_vhd_files_src)
    add_to_list(uvvm_light_list, util_vhd_files_target)

    print("Searching for PDF and PPS files. ", end='')
    util_doc_files_src = [f for f in glob.glob("./uvvm_public/uvvm_util/doc/*.pdf")]
    util_doc_files_src += [f for f in glob.glob("./uvvm_public/uvvm_util/doc/*.pps")]
    util_doc_files_target = [item.replace("uvvm_public/uvvm_util/", "") for item in util_doc_files_src]
    print("Found: src=%i, target=%i." %(len(util_doc_files_src), len(util_doc_files_target)))
    
    add_to_list(uvvm_internal_list, util_doc_files_src)
    add_to_list(uvvm_light_list, util_doc_files_target)


    print("Creating list of all BFM vhd files available. ", end='')
    bfm_files_src_not_filtered = [filename for filename in glob.glob("./uvvm_public/bitvis_*/src/*bfm*.vhd")]
    bfm_files_target = [filename for filename in glob.glob("./src_bfm/*.vhd")]

    bfm_files_src_filtered = remove_not_listed(bfm_files_src_not_filtered, bfm_files_target)
    print("Found: src=%i, target=%i." %(len(bfm_files_src_filtered), len(bfm_files_target)))

    add_to_list(uvvm_internal_list, bfm_files_src_filtered)
    add_to_list(uvvm_light_list, bfm_files_target)

    print("SKIPPING - DUT adapted to run with TB and updating DUT will make TB fail!\n Creating list of IRQC src files available.")
    #demo_files_src = [filename for filename in glob.glob("./uvvm_public/bitvis_irqc/src/*.vhd")]
    #demo_files_target = [filename for filename in glob.glob("./demo_tb/dut/*.vhd")]
    #print("Found: src=%i, target=%i." %(len(demo_files_src), len(demo_files_target)))
    #add_to_list(uvvm_internal_list, demo_files_src)
    #add_to_list(uvvm_light_list, demo_files_target)


    present_files(uvvm_internal_list, uvvm_light_list)
    copy_files(uvvm_internal_list, uvvm_light_list)


    print("\nTesting compilation and demo TB.")
    test_compilation()

    print("\nCleaning up repository.")
    cleanup("uvvm_public")

    print("\nPublishing release changes to GitHub")
    publish_github()


    print("==========================================================================")
    print(" UVVM_Light RELEASE DONE\n")



if __name__ == "__main__":
    main()