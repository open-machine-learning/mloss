VER=r$(shell svn info  | grep Revision | cut -f 2 -d ' ')
RELEASENAME:=mloss-$(VER)
RELEASETAR:=mloss-r$(shell svn info  | grep Revision | cut -f 2 -d ' ').tar.bz2
RELEASEDIR:=releases

WEBSITEDIR:=django

HOST=mloss.org

#get-live-db:
#	rm -f mloss/mloss.db
#	scp -P 65514 admintools/mysql_to_sqlite.sh mloss@zut.tuebingen.mpg.de:
#	cd mloss ; python manage.py syncdb --noinput
#	#( ssh mloss@zut.tuebingen.mpg.de chmod 700 mysql_to_sqlite.sh \; ./mysql_to_sqlite.sh ) >mloss/mloss.dump
#	( ssh -p 65514 mloss@zut.tuebingen.mpg.de chmod 700 mysql_to_sqlite.sh \; ./mysql_to_sqlite.sh ) | sqlite3 mloss/mloss.db
#	ssh -p 65514 mloss@zut.tuebingen.mpg.de rm -f mysql_to_sqlite.sh
#
release: clean
#	svn commit
	svn update
	rm -rf $(RELEASEDIR)/$(RELEASENAME)
	svn export mloss $(RELEASEDIR)/$(RELEASENAME)
	ssh mloss@${HOST} rm -rf $(WEBSITEDIR)/$(RELEASENAME) 
	tar cjvf - -C releases --exclude 'mloss.db' $(RELEASENAME) | \
		ssh mloss@${HOST} \
		\( tar -xjvf - -C $(WEBSITEDIR) \; sync \; sync \; sync \; \
		sed -i "s#XXXXXXXXX#\`cat /home/mloss/.mysql_password\`#" $(WEBSITEDIR)/$(RELEASENAME)/settings.py \; \
		sed -i '"s/^PRODUCTION = False/PRODUCTION = True/g"' $(WEBSITEDIR)/$(RELEASENAME)/settings.py \; \
		python -mcompileall $(WEBSITEDIR)/$(RELEASENAME)/ \; \
		find $(WEBSITEDIR)/$(RELEASENAME) -type d -exec chmod 755 {} '\;' \; \
		find $(WEBSITEDIR)/$(RELEASENAME) -type f -exec chmod 644 {} '\;' \; \
		chmod 640 $(WEBSITEDIR)/$(RELEASENAME)/settings.py\* \; \
		cp $(WEBSITEDIR)/$(RELEASENAME)/media/css/base.css static/media/css/base.css \; \
		chmod 644 static/media/css/base.css \; \
		cd $(WEBSITEDIR) \; ln -snf $(RELEASENAME) mloss \; \
		chmod 755 /home/mloss/bin/update_*.sh \; \
		sudo /etc/init.d/fapws3 restart \
		\)
	rm -rf $(RELEASEDIR)/$(RELEASENAME)

tar: clean
	rm -rf "$(RELEASEDIR)/$(RELEASENAME)"
	svn export mloss $(RELEASEDIR)/$(RELEASENAME)
	cd $(RELEASEDIR) && tar cjvf $(RELEASETAR) $(RELEASENAME)
	rm -rf "$(RELEASEDIR)/$(RELEASENAME)"

clean:
	find ./ -name '*.pyc' -delete
	find ./ -name '*.swp' -delete
