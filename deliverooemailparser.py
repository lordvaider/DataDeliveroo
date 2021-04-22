from datetime import datetime
import deliverooemailparsertxt as dept


def get_dt(msg):
    # Extract date time from email header and convert to right format

    return datetime.strptime(msg.get('Date'), '%a, %d %b %Y %H:%M:%S %z')


def unit_or_total(tab, bls):
    # check if the price is unit or total

    utot = sum(tab.Qty*tab.Price)
    ttot = sum(tab.Price)
    atot = float(bls['Subtotal'])

    if abs(atot - ttot) < abs(atot - utot):
        return 'Total'
    else:
        return 'Unit'


def format_orders_tab(tab, dt, r, bls):
    # Add the right column names and format strings
    # bls = bottomlines, used to figure out if the prices are perunit or total

    tab['Date'] = dt
    tab['Restaurant'] = r

    tab['Qty'] = [int(x.replace('x', '')) for x in tab.Qty]
    tab['Price'] = [float(x.replace('=C2=A3', '')) for x in tab.Price]

    tab['Price Convention'] = unit_or_total(tab, bls)

    tab = tab[['Date', 'Restaurant', 'Item', 'Qty', 'Price', 'Price Convention']]

    return tab


def get_data_from_email(email):
    # Accepts data in the 'email' format and returns a dataframe with rest, time, and orders

    # get date time from header
    dt = get_dt(email)

    # try:
    # hr, hos = deph.get_data_from_html(email, dt)
    # except:

    r, os, bls = dept.get_data_from_text(email)

    os = format_orders_tab(os, dt, r, bls)

    return os