import urllib
from xml.dom import minidom
from software.models import Software
from django.contrib.auth.models import User



class CRANPackage:
    """
    Modelling a software package in CRAN
    http://cran.r-project.org/
    """
    name = ""
    url = ""
    description_url = ""    
    is_core = False
    cran_text = ""

    decription = ""
    os_license = ""
    version = ""

    def __init__(self,node_value):
        self.name = node_value
        self.url = 'http://cran.r-project.org/package=' + self.name
        self.description_url = 'http://cran.r-project.org/web/packages/'+self.name+'/DESCRIPTION'

    def __repr__(self):
        return (self.name, self.url, self.cran_text, self.description_url, self.is_core)

    def parse_cran_text(self):
        """
        Read the data at description_url and save it to description
        Parse the text description from CRAN (in debian control file format)
        and return a dictionary.
        """
        usock = urllib.urlopen(self.description_url)
        self.cran_text = usock.read()
        usock.close()

        cran_dict = {}
        all_lines = self.cran_text.split('\n')
        curkey = None
        for line in all_lines:
            if line != '' and (line[0] == ' ' or line[0] == '\t'):
                curval += ' ' + line.strip()
            else:
                if curkey is not None:
                    cran_dict[curkey] = curval
                if line == '':
                    continue
                kv = line.split(':')
                curkey = kv[0]
                curval = kv[1].strip()   # this doesn't work for url
                
        self.os_license = cran_dict['License'].strip()
        self.version = cran_dict['Version'].strip()
        if cran_dict.has_key('Title'):
            self.description = cran_dict['Title'] + ': ' + cran_dict['Description']
        else:
            self.description = cran_dict['Bundle'] + ': ' + cran_dict['BundleDescription']

    def insert_into_database(self):
        """
        For a given CRANPackage construct Software object and insert it into database
        """
        # check whether the package exists
        dbpkg = Software.objects.filter(title=self.name)
        if dbpkg.count() == 0:
            # Hard code that Cheng submits software.
            me = User.objects.filter(username='ong')[0]

            # if not create a new Software project
            spkg = Software(user=me, title=self.name, version=self.version,
                            description=self.description, os_license=self.os_license,
                            language='R', operating_systems='agnostic',
                            download_url=self.url, tags='auto from cran')
        else:
            print 'Package ' + self.name + ' found, UPDATING...'
            assert(dbpkg.count() == 1)
            spkg = dbpkg[0]
            # Don't mess around with manual entries.
            if spkg.tags == 'auto from cran':
                return
            spkg.version = self.version
            spkg.description = self.description
            spkg.os_license = self.os_license
            spkg.download_url = self.url
        spkg.save()


def parse_ctv():
    """
    Parse
    http://cran.r-project.org/web/views/MachineLearning.ctv
    and generate a list of CRANPackage.
    """
    url = 'http://cran.r-project.org/web/views/MachineLearning.ctv'
    usock = urllib.urlopen(url)
    xmldoc = minidom.parse(usock)
    usock.close()
    plist = xmldoc.getElementsByTagName('packagelist')[0]
    packages = plist.getElementsByTagName('pkg')
    cpkglist = []
    for pkg in packages:
        cpkg = CRANPackage(pkg.childNodes[0].nodeValue)
        if len(pkg.attributes.keys())==1:
            assert(pkg.attributes.keys()[0]=='priority')
            assert(pkg.attributes['priority'].value == 'core')
            cpkg.is_core = True
        else:
            assert(len(pkg.attributes.keys())==0)
        cpkglist.append(cpkg)
    return cpkglist
        

def main():
    """Slurp projects from CRAN"""
    cpkglist = parse_ctv()
    for pkg in cpkglist:
        print pkg.name
        pkg.parse_cran_text()
        pkg.insert_into_database()
