#!/bin/bash
touch /etc/rc.local
chown root /etc/rc.local
chmod 755 /etc/rc.local
echo "gvm-start
wait
gvm-start
wait
python3 /opt/Afstudeerproject/flask/app.py" > rc.local
crontab -l | { cat; echo "0 0 1 0 0 gvm-feed-update"; } | crontab -
git clone https://github.com/TiboDeClercq/Afstudeerproject.git /opt/
apt install ufw
ufw allow 5000
ufw allow 9392
ufw enable
