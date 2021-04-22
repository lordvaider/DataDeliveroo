# Importing libraries
import imaplib
import deliverooemailparser as dep
import pandas as pd
import email

user = 'example@gmail.com'
password = 'yourpassword'
imap_url = 'imap.gmail.com'


# Function to search for a key value pair
def search(key, value, con):
    result, data = con.search(None, key, ' "{}"'.format(value))
    return data


def fetch_msgs():
    # this is done to make SSL connection with GMAIL
    con = imaplib.IMAP4_SSL(imap_url)

    # logging the user in
    con.login(user, password)

    # calling function to check for email under this label
    con.select('Inbox')

    # fetching emails noreply@t.deliveroo.com info@deliveroo.co.uk
    result, raw = con.search(None, """(SUBJECT "in the kitchen" SENTON "24-JUL-2020")""")
    # result, raw = con.search(None, """(SUBJECT "in the kitchen")""")
    # result, raw = con.search(None, """(SUBJECT "has accepted your order" SENTON "05-APR-2019")""")
    # result, raw = con.search(None, """(SUBJECT "has accepted your order" SENTON "31-DEC-2019")""")
    # result, raw = con.search(None, """(SUBJECT "in the kitchen" SENTON "05-DEC-2020")""")
    # result, raw = con.search(None, """(SUBJECT "has accepted your order" SENTON "26-AUG-2018")""")
    # result, raw = con.search(None, """(SUBJECT "has accepted your order")""")
    # result, raw = con.search(None, """(FROM "noreply@t.deliveroo.com")""")
    msgs = []  # all the email data are pushed inside an array

    for num in raw[0].split():
        _, data = con.fetch(num, '(RFC822)')
        msb = email.message_from_bytes(data[0][1])
        msgs.append(msb)

    return msgs


def main():
    msgs = fetch_msgs()
    orders = []
    for (i, msg) in enumerate(msgs):
        print('Parsing email number ', i)
        try:
            orders.append(dep.get_data_from_email(msg))
        except:
            print('!!!!!Encountered error while trying to parse email ', i, '!!!!!')

    df = pd.concat(orders).reset_index(drop=True)
    df.to_csv('Deliveroo2 txt')


main()
