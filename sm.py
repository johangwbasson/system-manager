import argparse
import json
import subprocess
from os import path

def newConfig():
    return {'packages': { 'install': [], 'uninstall': []}}

def loadConfig():
    try:
        if path.exists('system.json'):
            with open('system.json') as f:
                return json.load(f)
        return newConfig()                
    except IOError:        
        return newConfig()

def writeConfig(cfg):
    try:
        f = open('system.json', 'w')
        f.write(json.dumps(cfg, indent=4, sort_keys=True))        
        f.close()
    except IOError:
        print("Error: Unable to write configuration to file")

def installPackage(pkg):
    proc = subprocess.Popen(['sudo', 'pacman', '-S', pkg], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = proc.communicate()
    if 'error: target not found:' in stderr.decode('utf-8'):
        proc = subprocess.Popen(['yay', '-S', pkg], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if 'Could not find all required packages' in stderr.decode('utf-8'):
            print("Error: Package %s not found" % pkg)
            return False
    print("Package %s installed" % pkg)
    return True

def removePackage(pkg):
    result = subprocess.run(['sudo', 'pacman', '-R', pkg], stdout=subprocess.PIPE)
    if 'error: target not found:' in result.stdout.decode('utf-8'):
        result = subprocess.run(['yay', '-R', pkg], stdout=subprocess.PIPE)
        if 'error: target not found:' in result.stdout.decode('utf-8'):
            print("Error: Package %s is not installed" % pkg)
            return False
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", help="Add package")
    parser.add_argument("-r", help="Remove package")
    parser.add_argument("-s", help="Sync system packages to config file")
    args = parser.parse_args()
    data = loadConfig()

    if args.a:        
        if args.a not in data['packages']['install']:
            if (installPackage(args.a)):
                if args.a in data['packages']['uninstall']:
                    data['packages']['uninstall'].remove(args.a)
                data['packages']['install'].append(args.a)
                writeConfig(data)
            

    if args.r:
        if args.r not in data['packages']['uninstall']:
            if (removePackage(args.r)):
                if args.r in data['packages']['install']:
                    data['packages']['install'].remove(args.r)
                data['packages']['uninstall'].append(args.r)
                writeConfig(data)
    
    if args.s:
        print("Installing packages")
        for pkg in data['packages']['install']:
            installPackage(pkg) 
        
        print("Removing packages")
        for pkg in data['packages']['uninstall']:
            removePackage(pkg)

main()
