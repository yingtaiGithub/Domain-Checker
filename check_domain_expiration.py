import re

import whois
import pythonwhois
from datetime import datetime
from sys import exit

def check1(domain):
    now = datetime.now()
    try:
        w = whois.whois(domain)
    except UnicodeError:
        return "Wrong Domain Name"

    if (w.expiration_date and w.status) == None:
        # print ('The domain does not exist, exiting...')

        return None

    if type(w.expiration_date) == list:
        w.expiration_date = w.expiration_date[0]
    else:
        w.expiration_date = w.expiration_date

    domain_expiration_date = str(w.expiration_date.year) + '-' + str(w.expiration_date.month) + '-' + str(w.expiration_date.day)

    # timedelta = w.expiration_date - now
    # days_to_expire = timedelta.days
    #
    # if timedelta.days <= 60 and timedelta.days > 30:
    #     print ('WARNING: %s is going to expire in %s days, expiration date is set to %s' % (domain, days_to_expire, domain_expiration_date))
    #     exit(1)
    # elif timedelta.days <= 30:
    #     print ('WARNING: %s is going to expire in %s days, expiration date is set to %s' % (domain, days_to_expire, domain_expiration_date))
    #     exit(2)
    # else:
    #     print ('OK, the domain %s is expiring on %s, %s days to go. No need to renew at this moment of time' % (domain, domain_expiration_date, days_to_expire))
    #     exit(0)
    return domain_expiration_date


def check(domain):
    try:
        detail = pythonwhois.get_whois(domain)
    except UnicodeError:
        return "Wrong Domain Name"

    # print (detail)

    if 'expiration_date' in detail:
        domain_expiration_date = detail['expiration_date'][0]
        print (type(domain_expiration_date))
        domain_expiration_date = domain_expiration_date.strftime("%Y-%m-%d")
    elif 'No match for' in detail['raw'][0]:
        domain_expiration_date = "No match for %s" %domain
    elif 'domain_datebilleduntil' in detail['raw'][0]:
        domain_expiration_date = re.search(r'domain_datebilleduntil: ([0-9-]+)T', detail['raw'][0]).group(1)
    else:
        domain_expiration_date = "None"

    return domain_expiration_date


def main():
    # domain = "google.com"
    # domain = "reeves.co.nz"
    # domain = "reeves.nz"
    # domain = "aaaaaazzccdeedfdssedf1234.com"
    # domain = "google.com.au"
    # domain = "Spotless.com.au"
    # domain = "Localhost.co.nz"
    # domain = "Reeves.net.nz"
    domain = "Matthewgallagher.net.au"
    print (check(domain))

if __name__ == "__main__":
    main()