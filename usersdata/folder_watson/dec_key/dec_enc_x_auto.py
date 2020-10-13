server_block = '''
server {
    listen       80 default_server;
    # listen       [::]:80 default_server;
    server_name %s;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root %s;
    }

    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://unix:%s/myproject.sock;
    }
'''(server_domain_ip, staticfiles_path, )













with open('nginx.txt', 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('''server {
        listen       80 default_server;
        # listen       [::]:80 default_server;
        server_name  _;
        root         /usr/share/nginx/html;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        location / {
        }''', '''server {
    listen       80 default_server;
    # listen       [::]:80 default_server;
    server_name some.domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root /home/ayush/myproject;
    }

    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://unix:/home/ayush/myproject/myproject.sock;
    }''')

# Write the file out again
with open('nginx.txt', 'w') as file:
  file.write(filedata)