import sys
import time
import smtplib
from email.mime.text import MIMEText

import config
from app import db, Domain, save_domain
import check_domain_expiration


def send_email(body):
    # emails = [item.strip() for item in to_email.split(",")]
    msg = body
    msg = MIMEText(msg)
    msg['Subject'] = 'DOMAIN CHECK'
    msg['From'] = config.email
    msg['To'] = config.email

    if '@gmail' in msg['From']:
        s = smtplib.SMTP('smtp.gmail.com', 587)
    elif '@outlook.com' in msg['From']:
        s = smtplib.SMTP('smtp.live.com', 	587)
    else:
        print ('The sender email must be gmail or hotmail')
        sys.exit()

    s.ehlo()
    s.starttls()
    s.ehlo()

    # if not emails:
    #     return

    try:
        s.login(config.email, config.password)
    except Exception as e:
        print ("LOGIN ERROR\n")
        print (e)
        sys.exit(2)

    try:
        # for email in emails:
        #     if email:
        #         s.sendmail(config.from_email, email, msg.as_string())
        s.sendmail(config.email, config.email, msg.as_string())
    except:
        print ("Invaid email")
        sys.exit(3)

    s.quit()

def main():
    # domains = Domain.query.filter(Domain.name != None).all()
    domains = Domain.query.all()

    data = []
    for domain in domains:
        expire_date = check_domain_expiration.check(domain.name)
        if expire_date != "Wrong Format" and expire_date:
            save_domain({'name': domain.name, 'expire_date': expire_date})
            data.append({'name': domain.name, 'expire_date': expire_date})

        time.sleep(5)

    send_email(str(data))

if __name__ == "__main__":
    main()
