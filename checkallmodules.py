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
                #Node export,Node export relation (deprecated) (node_export_relation),Not installed,7.x-3.1
                names = linelist[1].split('(')
                if len(names)>2:
                    #this recreates the module and correctly generates the machine name if there is a parenthesis in the module display name
                    machinename = names[-1].strip(')')
                    modulename = names[0]
                    for chars in names[1:-1]:
                        modulename = modulename + "("+chars

                else:
                    modulename = names[0].strip()
                    machinename = names[1].strip(')')

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

    here = '/home/dlb213/usedscripts/check_installedmodules'
    os.chdir(here)
                
    print "reading in CAS2 modules"
    cas2file = open('cas2modules.csv','r')
    cas2modules = parsemodulelist(cas2file,version)
    cas2file.close()

    print "reading in CAS3 modules"
    cas3file = open('cas3modules.csv','r')
    cas3modules = parsemodulelist(cas3file,version)
    cas3file.close()

    #I am also going to add a file here for checking that all of the modules on the default database are also on the site

    #now get the currently installed modules on this server

    #backup the old list, why not
    now = datetime.datetime.now()
    os.system('mv currentmodulelist.csv modulelistbackups/currentmodulelist-'+now.strftime('%m%d%y%H%M')+'.csv')
    print "generating current module list"
    os.chdir('/var/www/drupal/sites/')
    os.system('drush pm-list --type=module --format=csv > /home/dlb213/usedscripts/check_installedmodules/currentmodulelist.csv')

    os.chdir(here)
    print "reading in current module list"
    listfile = open('currentmodulelist.csv','r')
    modulelist = parsemodulelist(listfile,version)
    listfile.close()

    missunion = {}
    missintersection = {}
    #now I guess loop through each cas2 and cas3 list and see which are the same.
    print ""
    print " -------------  PRINTING CAS 2  MISSING MODULES --------------------- "
    print ""
    misscas2 = {}
    for cas2 in sorted(cas2modules):
        if cas2 not in modulelist.keys():
            misscas2[cas2] = cas2modules[cas2]
            missunion[cas2] = cas2modules[cas2]
            print cas2modules[cas2][0]+" -- "+cas2

    print ""
    print " -------------  PRINTING CAS 3  MISSING MODULES --------------------- "
    print ""
    misscas3 = {}
    for cas3 in sorted(cas3modules):
        if cas3 not in modulelist.keys():
            misscas3[cas3] = cas3modules[cas3]
            print cas3modules[cas3][0]+" -- "+cas3
            if cas3 in missunion.keys():
                missintersection[cas3] = cas3modules[cas3]
            else:
                missunion[cas3] = cas3modules[cas3]
                
    print ""
    print " ------------- MODULES MISSING UNION FROM BOTH SERVERS--------------------- "
    print ""            
    
    for u in sorted(missunion):
        print missunion[u][0]+" -- "+u

        
    print ""
    print " ------------- MODULES MISSING INTERSECTION FROM BOTH SERVERS--------------------- "
    print ""            
    
    for i in sorted(missintersection):
        print missintersection[i][0]+" -- "+i

    
            
    # I could add a flag to the script that checks the version of the modules in the other lists and prints out the comparisons.
    # To Do this look for python command flag integration libraries


if __name__ == "__main__":
    main()
