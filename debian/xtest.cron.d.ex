#
# Regular cron jobs for the xtest package
#
0 4	* * *	root	[ -x /usr/bin/xtest_maintenance ] && /usr/bin/xtest_maintenance
