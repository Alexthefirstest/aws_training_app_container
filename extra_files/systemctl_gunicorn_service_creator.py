import subprocess

file_content = """[Unit]
Description=autostart gunicorn with aws_training_app
After=network.target

[Service]
WorkingDirectory=/usr/local/bin/aws_training_app
ExecStart={0} -w 4 -b localhost:8000 'source.web:main_flask'

[Install]
WantedBy=multi-user.target"""

p = subprocess.run(r'find /home/ec2-user/.local/share/virtualenvs/*/bin -name gunicorn',
                   capture_output=True, shell=True)
res = p.stdout.decode().split('\n')[0]
print('script_res:', res)

with open("aws_app_g.service", "w") as f:
    f.write(file_content.format(res))
