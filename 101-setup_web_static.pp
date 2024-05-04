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

file { 'test_dir':
  ensure => 'directory',
  path   => '/data/web_static/releases/test/',
}

file { 'shared_dir':
  ensure => 'directory',
  path   => '/data/web_static/shared',
}

file { 'index_html':
  ensure  => 'file',
  path    => '/data/web_static/releases/test/index.html'
  content => '<html>
      <head>
      </head>
      <body>
          Holberton School
      </body>
</html>',
}

file { 'symlink':
  ensure => 'link',
  path   => '/data/web_static/current',
  target => '/data/web_static/releases/test/'
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