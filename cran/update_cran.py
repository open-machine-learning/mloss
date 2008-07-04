import urllib
import datetime
import time
import sys
import os
import re

if os.environ['HOME'].endswith('/mloss'):
    sys.path.insert(0, '/home/mloss')
    sys.path.insert(0, '/home/mloss/mloss')
    sys.path.insert(0, '/home/mloss/lib/python2.5/site-packages')
else:
    sys.path.insert(0, '/home/sonne/Documents/work/first/repositories/mloss/website/mloss')
    sys.path.insert(0, '/home/sonne/Documents/work/first/repositories/mloss/website/mloss/mloss')
os.environ['DJANGO_SETTINGS_MODULE']='mloss.settings'

from xml.dom import minidom
from software.models import Software
from django.contrib.auth.models import User
import settings

class CRANPackage:
    """
    Modelling a software package in CRAN
    http://cran.r-project.org/
    """
    prefix="r-cran-"
    name = ""
    url = ""
    author = ""
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

    def convert_date(self, date):
        """
        Try various ways to grab a valid date from the R DESCRIPTION file
        """
        if date:
            try:
                self.date=datetime.datetime(*time.strptime(date, "%Y-%m-%d")[:5])
            except ValueError:
                pass

            if self.date is None:
                try:
                    self.date=datetime.datetime(*time.strptime(date, "%d/%m/%Y")[:5])
                except ValueError:
                    pass

            if self.date is None:
                try:
                    self.date=datetime.datetime(*time.strptime(date, "%Y/%m/%d")[:5])
                except ValueError:
                    pass

            if self.date is None:
                try:
                    self.date=datetime.datetime(*time.strptime(date)[:5])
                except ValueError:
                    pass

    def convert_license(self, license):
        """
        Licenses in R are usually very compact strings, like GPL-2 etc.
        Now '-' is an illegal letter on mloss.org tags (causing name clashes)
        Try to come up with a mapping for licenses
        """
        license=license.strip().lower()
        license_hash= {
                'gpl' : 'gpl',
                'gpl (>= 2)' : 'gpl version 2 or later',
                'gpl (>=2)' : 'gpl version 2 or later',
                'gpl-2' : 'gpl version 2',
                'gpl 2.0' : 'gpl version 2',
                'gpl2.0' : 'gpl version 2',
                'gpl-2 | file licence' : 'gpl version 2',
                'gpl-2 | gpl-3' : 'gpl version 2 or later',
                'gpl-3' : 'gpl version 3',
                'gpl version 2' : 'gpl version 2',
                'gpl (version 2 or later)' : 'gpl version 2 or later',
                'gpl version 2 or later' : 'gpl version 2 or later',
                'gpl (version 2 or newer)' : 'gpl version 2 or later',
                'gpl version 2 or newer' : 'gpl version 2 or later',
                'lgpl' : 'lgpl',
                'pl (>=2)' : 'gpl version 2 or later',
                'use under gpl2, or see file licence' : 'gpl version 2'}
        try:
            license=license_hash[license]
        except KeyError:
            pass
        self.os_license = license

    def convert_author(self, author):
        author,count = re.subn(r'<[^\s].*>', "", author,100)
        author,count = re.subn(r'Material from the book.s webpage, R port and packaging by ', "", author,100)
        author,count = re.subn(r'[\s]&', ",", author,100)
        author,count = re.subn(r'[\s]and', ",", author,100)
        author,count = re.subn(r'R port by ', "", author,100)
        author,count = re.subn(r'rpart by ', "", author,100)
        author,count = re.subn(r', Jr', " Jr", author,100)
        author,count = re.subn(r'; port to R, tests etc:', ",", author,100)
        author,count = re.subn(r'[Oo]riginal by ', "", author,100)
        author,count = re.subn(r'[Cc]ontributions from ', "", author,100)
        author,count = re.subn(r'with contributions (by|from) ', "", author,100)
        author,count = re.subn(r'following earlier work (by|from) ', "", author,100)
        author,count = re.subn(r'derived from [^\s].* by ', ",", author,100)
        author,count = re.subn(r'with ', "", author,100)
        author,count = re.subn(r'\s\.', ",", author,100)
        author,count = re.subn(r'(,,|\s,)', ",", author,100)
        author,count = re.subn(r'[\.,]?\s*$', "", author,100)
        author,count = re.subn(r'([^\s]){2}\.', r'\1,', author,100)
        self.author=author

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
                idx=line.index(':')
                curkey = line[:idx]
                curval = line[(idx+2):].strip()
        if curkey is not None:
            cran_dict[curkey] = curval

        self.date=None
        try:
            self.convert_date(cran_dict['Date'])
        except KeyError:
            pass

        if self.date is None:
            try:
                self.convert_date(cran_dict['Packaged'].split(';')[0])
            except KeyError:
                pass

        if self.date is None:
            self.date = datetime.datetime.now()

        self.convert_license(cran_dict['License'])
        self.version = cran_dict['Version'].strip()
        self.convert_author(cran_dict['Author'])
        if cran_dict.has_key('Title'):
            self.description = cran_dict['Title'] + ': ' + cran_dict['Description']
        else:
            self.description = cran_dict['Bundle'] + ': ' + cran_dict['BundleDescription']

    def insert_into_database(self):
        """
        For a given CRANPackage construct Software object and insert it into database
        """
        try:
            me = User.objects.get(username=settings.R_CRAN_BOT)
        except User.DoesNotExist:
            user = User.objects.create_user(settings.R_CRAN_BOT, settings.R_CRAN_BOT + '@mloss.org', 'xdf46i07XGTASGDTGEIjtrt')
            user.save()
            me = User.objects.get(username=settings.R_CRAN_BOT)


        #don't insert crappy items having future date
        if self.date<datetime.datetime.now():
            # check whether the package exists (without prefix)
            dbpkg = Software.objects.filter(title=self.name)
            if dbpkg.count() > 0:
                return

            # check whether the package exists (without prefix)
            dbpkg = Software.objects.filter(user=me, title=self.prefix+self.name)
            if dbpkg.count() == 0:
                # if not create a new Software project
                spkg = Software(user=me, title=self.prefix+self.name, version=self.version,
                                description=self.description, os_license=self.os_license,
                                language='R', operating_systems='agnostic',
                                download_url=self.url, project_url=self.url, tags='r-cran',
                                pub_date=self.date, updated_date=self.date, authors=self.author)
                spkg.save(False)
            else:
                #print 'Package ' + self.name + ' found, UPDATING...'
                assert(dbpkg.count() == 1)
                spkg = dbpkg[0]
                # Don't mess around with manual entries.
                if spkg.tags != 'r-cran':
                    return
                spkg.version = self.version
                spkg.description = self.description
                spkg.os_license = self.os_license
                spkg.download_url = self.url
                spkg.project_url = self.url
                spkg.updated_date=self.date
                spkg.authors=self.author
                spkg.save(False)


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

"""Slurp projects from CRAN"""
cpkglist = parse_ctv()
for pkg in cpkglist:
    pkg.parse_cran_text()
    print pkg.name, pkg.author
    pkg.insert_into_database()
