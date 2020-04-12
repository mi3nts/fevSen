
#!/bin/bash
#

kill $(ps aux | grep jetsonSaverMarch20.py | awk '{print $2}' | head -1)
kill $(ps aux | grep jetsonReaderMarch20.py | awk '{print $2}' | head -1)
