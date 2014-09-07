server {
auth_basic "Restricted";
auth_basic_user_file htpasswd;

listen 80;
server_name {{ server_name }};
access_log /var/log/nginx/docker_access.log;
error_log /var/log/nginx/docker_error.log;
proxy_redirect off;
proxy_buffering off;
proxy_set_header Host \$host;
proxy_set_header X-Real-IP \$remote_addr;
proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
location / {
include uwsgi_params;
uwsgi_pass 127.0.0.1:{{ uwsgi_port }};
}
location /static {
root {{ public_folder }};
}
location /media {
root {{ public_folder }};
}
}
