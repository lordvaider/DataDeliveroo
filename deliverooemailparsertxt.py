import re
import pandas as pd


def clean_resplit_result(rr):
    # does some basic cleaning on the result of a deliveroo email regex match

    return [x.strip(' -') for x in rr if len(x.strip(' ')) > 0 and not x == '=C2=A3']


def get_bl(field, tlist):
    # Gets the value of the bottom line field "field"

    p = re.compile(".*({}).*?(=C2=A3|)([0-9]+[.][0-9]{{2}})$".format(field))

    bll = [x for x in tlist if bool(re.match(p, x))]
    if len(bll):
        bl = re.split(p, bll[0])
        bl = clean_resplit_result(bl)
        return bl[1]
    else:
        return 0


def get_bls(tlist):
    # Gets the bottom line attributes from the meial

    blfs = ['Subtotal', 'Delivery fee', 'Small order fee', 'Tip', 'Credit', 'Total']
    bls = {}
    for f in blfs:
        bls[f] = get_bl(f, tlist)

    return bls


def get_restaurant_txt(tlist):
    p = re.compile('(.*)has (|accepted |received )your order')
    rs = [x for x in tlist if bool(re.match(p, x))][0]
    r = re.split(p, rs)
    return r[1].strip(" ")


def get_orders_txt(tlist):
    p = re.compile(".*([0-9]+)x(.*?)(=C2=A3|)([0-9]+[.][0-9]{2})$")
    ol = [x for x in tlist if bool(re.match(p, x))]
    oda = []
    for o in ol:
        oa = re.split(p, o)
        oa = clean_resplit_result(oa)
        oda.append({'Qty': oa[0], 'Item': oa[1], 'Price': oa[2]})

    return pd.DataFrame(oda)


def get_data_from_text(email):
    # extract text string
    tbody = [x for x in email.walk() if x.get_content_type() == 'text/plain'][0].get_payload()

    # convert tbody to list of lines
    tbody = tbody.replace('=0D=', '')
    tbody = tbody.replace('=0D', '')
    tlist = tbody.split('\r\n')

    r = get_restaurant_txt(tlist)

    os = get_orders_txt(tlist)

    bls = get_bls(tlist)

    return r, os, bls