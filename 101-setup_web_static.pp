File Edit Options Buffers Tools Help
# This manifest installs nginx on a webserver and
# configures the /hbnb_static location in the nginx
# config file.

exec { 'update_apt':
  command  => '/usr/bin/sudo /usr/bin/apt update',
}

package { 'nginx_installer':
  name     => 'nginx',
  provider => 'apt',
}

exec { 'test_dir':
     command  => 'sudo mkdir -p /data/web_static/releases/test/',
     provider => shell,
}

exec { 'shared_dir':
  command  => 'sudo mkdir -p /data/web_static/shared',
  provider => shell,
}

exec {'create_index':
     command  => 'echo "<html>\n\t<head>\n\t</head>\n\t<body>\n\t\tHolberton School\n\t</body>\n</html>" | sudo tee /data/web_static/releas\
es/test/index.html',
     provider => shell,
}

exec { 'symlink':
     command  => 'sudo ln -sf /data/web_static/releases/test/ /data/web_static/current',
     provider => shell,
}

file { 'chown_grp':
  ensure  => 'directory',
  path    => '/data/',
  recurse => true,
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

file { 'config_file':
  path    => '/etc/nginx/sites-available/default',
  content => 'server {
    listen 80 default_server;
    listen [::]:80 default_server;
    root /var/www/html;
    server_name _;
    location /redirect_me {
        return 301 https://www.alxafrica.com/;
    }
    location /hbnb_static {
        alias /data/web_static/current/;
    }
    location / {
        try_files ${uri} ${uri}/ =404;
    }
}',
}

exec { 'restart_nginx':
  command  => '/usr/bin/sudo /usr/sbin/service nginx restart',
}