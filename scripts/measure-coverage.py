import subprocess, sys
import re

REQ_COVERAGE = 90
print 'Measuring coverage (need %d%%)...' % REQ_COVERAGE
output = subprocess.check_output("venv/bin/coverage report --omit='venv/*'", shell=True)

for row in output.split('\n'):
	m = re.search(r"([0-9]+)%", row)
	if m is None:
		continue
	n = int(m.group(1))
	if n < REQ_COVERAGE:
		print 'Insufficient coverage: \n%s' % row
		sys.exit(1)

print 'Pass.'
