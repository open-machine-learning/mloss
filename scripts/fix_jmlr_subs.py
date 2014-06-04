from revision.models import *
from software.models import *
from settings import *

count=0
for software in Software.objects.all():
	revisions = Revision.objects.filter(software=software).order_by('-revision')

	has_jmlr_since_rev=10000000000000
	jmlr_mloss_url=None

	for rev in revisions:
		if rev.jmlr_mloss_url is not None and rev.jmlr_mloss_url.startswith('http://'):
			count+=1
		if jmlr_mloss_url is not None:
			if  rev.revision<has_jmlr_since_rev:
				print "updating '%s' rev '%d' to have url '%s'" % (software.title, rev.revision, jmlr_mloss_url)
				rev.jmlr_mloss_url=jmlr_mloss_url
				rev.save(silent_update=True)
			continue

		if rev.jmlr_mloss_url is not None and rev.jmlr_mloss_url.startswith('http://'):
			has_jmlr_since_rev=rev.revision
			jmlr_mloss_url=rev.jmlr_mloss_url
print count
