import subprocess

def getCommitHash(abbreviated=True):
    hashValue = ''
    cmdLong = ['git', 'rev-parse', 'HEAD']
    cmdSort = ["git", "describe", "--always"]
    try:
        hashValue = subprocess.check_output(cmdSort if abbreviated else cmdLong).strip().decode('utf-8')
    except:
        print('WARNING: Can not get commit hash')

    return hashValue


def getBranchName():
    branchName = ''
    try:
        branchName = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip().decode('utf-8')
    except:
        print('WARNING: Can not get commit hash')

    return branchName


def getDescribe(options='--long'):
    desc = ''
    try:
        desc = subprocess.check_output(['git','describe', options]).strip().decode('utf-8')
    except:
        print('WARNING: Can not get commit hash')
        
    return desc