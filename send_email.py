import smtplib
import ssl
from email.message import EmailMessage
import yaml

from read_calendar import get_next_events_str

CONFIG_FILE = 'config.yaml'
with open(CONFIG_FILE, 'r') as f:
  config = yaml.safe_load(f)

msg = EmailMessage()
msg["From"] = config['USERNAME']
msg["To"] = config['TO']
msg["Subject"] = config['SUBJECT']
msg.set_content(get_next_events_str())

context = ssl.create_default_context()
with smtplib.SMTP_SSL(config['SMTP_SERVER'], config['SMTP_PORT'], context = context) as server:
  server.login(config['USERNAME'], config['PASSWORD'])
  server.send_message(msg)
