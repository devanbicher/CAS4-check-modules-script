import os,datetime
#import sys
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
    cas2file = open('cas2modules.csv','r')
    cas2modules = parsemodulelist(cas2file)
    cas2file.close()
    
    cas3file = open('cas3modules.csv','r')
    cas3modules = parsemodulelist(cas3file)
    cas3file.close()

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

    # I could add a flag to the script that checks the version of the modules in the other lists and prints out the comparisons.




if __name__ == "__main__":
    main()
