import subprocess, sys
import re

REQ_COVERAGE = 90
output = subprocess.check_output("venv/bin/coverage report", shell=True)

for row in output.split('\n'):
	m = re.search(r"([0-9]+)%", row)
	if m is None:
		continue
	n = int(m.group(1))
	if n < REQ_COVERAGE:
		print 'Insufficient coverage (<%s%%): \n%s' % (REQ_COVERAGE, row)
		sys.exit(1)

