import os,datetime, sys

#This checks the modules on this server and indicates which are missing from the other 2 servers

def parsemodulelist(modulefile):
    line = modulefile.readline()
    modules = {}
    
    while line:
        if line.strip() == "":
            line = modulefile.readline()
            continue
        else:
            linelist = line.split(',')
            package = linelist[0]
            #Access control,Block Access (block_access),Enabled,7.x-1.6
            modulename = linelist[1].split('(')[0].strip()
            machinename = linelist[1].split('(')[1].strip(')')
            status = linelist[2]
            version = linelist[3].strip()
            line = modulefile.readline()
            modules[machinename] = [modulename,version,status,package]
            line = modulefile.readline()

    return modules
            


def main():

    version = false
    if len(sys.argv) > 1:
        if sys.argv[1].startswith('--'):
            if sys.argv[1] == '--version':
                version = true
                
    
    cas2file = open('cas2modules.csv','r')
    cas2modules = parsemodulelist(cas2file)
    cas2file.close()
    
    cas3file = open('cas3modules.csv','r')
    cas3modules = parsemodulelist(cas3file)
    cas3file.close()

    #I am also going to add a file here for checking that all of the modules on the default database are also on the site
    
    #now get the currently installed modules on this server
    os.chdir('/var/www/drupal/sites/')
    #backup the old list, why not
    now = datetime.datetime.now()
    os.system('mv currentmoduelist.csv modulelistbackups/currentmodulelist-'+now.strftime('%m%d%y%H%M')+'.csv')
    os.system('drush pm-list --type=module --format=csv > /home/dlb213/usedscripts/check_installedmodules/currentmodulelist.csv')

    listfile = open('currentmodulelist.csv','r')
    modulelist = parsemodulelist(listfile)
    listfile.close()

    #now I guess loop through each cas2 and cas3 list and see which are the same.

    for cas2 in sorted(cas2modules):
        if cas2 not in modulelist.keys():
            print cas2modules[cas2][0]+" ( "+cas2+" )  is on cas2, NOT on this server"
    
    # I could add a flag to the script that checks the version of the modules in the other lists and prints out the comparisons.
    # To Do this look for python command flag integration libraries


if __name__ == "__main__":
    main()
