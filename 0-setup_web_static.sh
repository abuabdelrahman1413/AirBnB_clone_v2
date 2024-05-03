#!/usr/bin/env bash
#This script sets up my web servers for the deployment of web_static.
sudo apt-get update
sudo apt-get install nginx -y
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared
echo "<html>
     <head>
     </head>
     <body>
	Holberton School
     </body>
</html>" | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/
conf="location /hbnb_static {
	       alias /data/web_static/current/
}
"
sudo sed -i "/server_name _;/a $conf/"
sudo service nginx restart
