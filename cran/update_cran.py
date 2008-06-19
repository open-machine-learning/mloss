import urllib
from xml.dom import minidom
from software.models import Software



class CRANPackage:
    """
    Modelling a software package in CRAN
    http://cran.r-project.org/
    """
    name = ""
    url = ""
    description = ""
    description_url = ""    
    is_core = False

    def __init__(self,node_value):
        self.name = node_value
        self.url = 'http://cran.r-project.org/package=' + self.name
        self.description_url = 'http://cran.r-project.org/web/packages/'+self.name+'/DESCRIPTION'

    def get_description():
        usock = urllib.urlopen(self.description_url)
        self.description = usock.read()
        usock.close()
        

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
        

def insert_into_database(cpkg):
    """
    For a given CRANPackage construct Software object and insert it into database
    """
    # How to deal with: user
    spkg = Software(title=cpkg.name, description=cpkg.get_description(),
                    language='R', operating_systems='agnostic',
                    download_url=cpkg.url)
    spkg.save()


    
