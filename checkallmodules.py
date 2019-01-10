import os,datetime, sys

#This checks the modules on this server and indicates which are missing from the other 2 servers

def parsemodulelist(modulefile,v):
    #set some variables up
    if v:
        lnlen = 3
    else:
        lnlen = 2
    modules = {}
    line = modulefile.readline()
    n=1
    while line:
        if line.strip() == "":
            line = modulefile.readline()
            n+=1
            continue
        else:
            linelist = line.split(',')
            if len(linelist)>lnlen and linelist[1].find('(')>0:
                package = linelist[0]
                #Access control,Block Access (block_access),Enabled,7.x-1.6
                modulename = linelist[1].split('(')[0].strip()
                machinename = linelist[1].split('(')[1].strip(')')
                status = linelist[2]

                if v:
                    version = linelist[3].strip()
                    modules[machinename] = [modulename,version,status,package]
                else:
                    modules[machinename] = [modulename,'--',status,package]
                #next line
                line = modulefile.readline()
                n+=1
            else:
                print "ERROR READING line "+str(n)+" printing line: "
                print line
                line = modulefile.readline()
                n+=1
                
    return modules
            


def main():

    version = False
    if len(sys.argv) > 1:
        if sys.argv[1].startswith('--'):
            if sys.argv[1] == '--version':
                version = True
                
    print "reading in CAS2 modules"
    cas2file = open('cas2modules.csv','r')
    cas2modules = parsemodulelist(cas2file,version)
    cas2file.close()

    print "reading in CAS3 modules"
    cas3file = open('cas3modules.csv','r')
    cas3modules = parsemodulelist(cas3file,version)
    cas3file.close()

    #I am also going to add a file here for checking that all of the modules on the default database are also on the site
    here=os.getcwd()
    #now get the currently installed modules on this server

    #backup the old list, why not
    now = datetime.datetime.now()
    os.system('mv currentmodulelist.csv modulelistbackups/currentmodulelist-'+now.strftime('%m%d%y%H%M')+'.csv')
    
    os.chdir('/var/www/drupal/sites/')
    os.system('drush pm-list --type=module --format=csv > /home/dlb213/usedscripts/check_installedmodules/currentmodulelist.csv')

    os.chdir(here)
    
    listfile = open('currentmodulelist.csv','r')
    modulelist = parsemodulelist(listfile,version)
    listfile.close()

    #now I guess loop through each cas2 and cas3 list and see which are the same.

    for cas2 in sorted(cas2modules):
        if cas2 not in modulelist.keys():
            print cas2modules[cas2][0]+" ( "+cas2+" )  is on cas2, NOT on this server"
    
    # I could add a flag to the script that checks the version of the modules in the other lists and prints out the comparisons.
    # To Do this look for python command flag integration libraries


if __name__ == "__main__":
    main()
