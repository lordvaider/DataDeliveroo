import re
import pandas as pd
from datetime import datetime
from functools import reduce


def get_dt(msg):
    # Extract date time from email header and convert to right format

    return datetime.strptime(msg.get('Date'), '%a, %d %b %Y %H:%M:%S %z')


def get_restaurant_tab(tabs):
    # take list of tables and extract rest name

    # extract string which contains restaurant name from list of dataframes
    p = re.compile('(.*)has (|accepted |received )your order')
    rs = [t for t in tabs if t.shape == (1, 1) and re.match(p, t[0][0])][0][0][0]
    rstnm = re.split("(.*)has your order!", rs)

    return rstnm[1].strip(" ")


def is_otab(tab):
    # check if a given table is an orders table

    # needs to have 3 columns
    if not(tab.shape[1] == 3):
        return False

    # first column is qtys = "<numbers>x"
    if not reduce(lambda x, y: x and bool(re.match("[0-9]+x", y)), tab[0]):
        return False

    # third column is prices "<pound symbol><numbers>.<numbers>"
    if not reduce(lambda x, y: x and bool(re.match("=C2=A3[0-9]+[.][0-9]{2}", y)), tab[2]):
        return False

    return True


def get_orders_tab(tabs):
    # list of tables -> table with order info
    otabs = [t for t in tabs if is_otab(t)]

    # if there are multiples just return the one with the most rows
    otab = max(otabs, key=lambda ot: ot.shape[0])
    otab.columns = ['Qty', 'Item', 'Price']

    return otab


def get_data_from_html(email, dt):
    # extract html body string
    hbody = [x for x in email.walk() if x.get_content_type() == 'text/html'][0].get_payload()

    # convert hbody to list of tables
    hbody = hbody.replace('=0D=', '')
    hbody = hbody.replace('=0D', '')
    tabs = pd.read_html(hbody)

    r = get_restaurant_tab(tabs)

    os = get_orders_tab(tabs)

    return r, os
