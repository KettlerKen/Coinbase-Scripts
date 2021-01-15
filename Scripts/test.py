import beautifultable
import requests
import cbpro
import json
import time
import sys
import os
import re
#from slackclient import SlackClient

MESSAGE_TIMEOUT = 600
QUERY_TIMEOUT = 10
public_client = cbpro.PublicClient()

coin_tickers = ["ETH-USD", "BTC-USD", "XLM-USD", "GRT-USD", "ATOM-USD"]

float_keys    = ['last', 'daily_change', 'open', 'high', 'low', 'volume']

formatted_table_rows = ['open', 'last']


def slack_message(message):
    wekbook_url = 'https://hooks.slack.com/services/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'

    data = {
        'text': message,
        'username': 'Mr. Robot',
        'icon_emoji': ':robot_face:'
    }

    response = requests.post(wekbook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    if response.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )


# def slack_message(message):
#     token = “xoxo-love”
#     sc = SlackClient(token)
#     print sc.api_call(“api.test”)
#     print sc.api_call(“im.open”, user=”U02EZLEIT”)


def test_change(data):
    print(data)
    return True


def main():
    rows, columns = os.popen('stty size', 'r').read().split()
    rows = int(rows)
    columns = int(columns)


    while True:
        formatted_table = ()
        formatted_table = beautifultable.BeautifulTable()
        formatted_table.columns.header = ['ticker'] + formatted_table_rows
        rows = []

        data_obj = []

        for ticker in coin_tickers:
            data = public_client.get_product_24hr_stats(ticker)
            row = []
            
            for key, value in data.items():
                if key in float_keys:
                    data[key] = float(data[key])

            data['daily_change'] = round((data['last'] - data['open']), 2)

            #print("======================== {} ========================".format(ticker))
            # for key, value in data.items():
            #     just_key = key.rjust(15, " ")
                # if key in keys_to_print:
                    #print("{}: ${}".format(just_key, value))

            row.append(ticker)
            for key in formatted_table_rows:
                row.append(data[key])

            rows.append(row)
            data_obj.append(data)
                
        for row in rows:
            formatted_table.append_row(row)   

        print(formatted_table)

        if test_change(data_obj):
            slack_message("```"+str(formatted_table)+"```")
            time.sleep(MESSAGE_TIMEOUT)

        time.sleep(QUERY_TIMEOUT)


if __name__ == "__main__":
    main()

