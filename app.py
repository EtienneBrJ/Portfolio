#!/usr/bin/python3
""" Application file

    Defining routes of the web application
"""
import config
from filters_builder import checkSeconds, fromTimestampToNow
from web3 import Web3
from flask import Flask, render_template
from funcs import getlatestBlocks, getlatestTxn

ws_provider = Web3.WebsocketProvider(config.MAINNET_WSS)
w3 = Web3(ws_provider)


app = Flask(__name__)

# Inbuilt function handling 404 error
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

# Routes
@app.route('/')
def index():
    """ Home page
        The homepage will display this info on the 5 latest block mined on the network:
                Block number:
                Miner:
                Block reward:
    """
    return render_template('index.html', last_blocks=getlatestBlocks(10), last_txn=getlatestTxn(10), miners=config.dict_miners)

@app.route('/blocks/')
@app.route('/block/<int:block_number>')
def block(block_number=None):
    """ Block page """
    if block_number:
        info_block = w3.eth.get_block(block_number)
        return render_template('block.html', block_number=block_number, info_block=info_block)
    return render_template('blocks.html', last_blocks=getlatestBlocks(10), miners=config.dict_miners)

@app.route('/transactions/')
@app.route('/transaction/<hash>')
def transaction(hash=None):
    """ Tx page """
    if hash:
        tx = w3.eth.get_transaction(hash)
        return render_template('transaction.html', hash=hash, tx=tx)
    return render_template('transactions.html', last_txn=getlatestTxn(10), last_block=getlatestBlocks(1))
    


@app.route('/address/')
@app.route('/address/<hexa_address>')
def address(hexa_address=None):
    """ Address page """
    if hexa_address:
        weiBalance = w3.eth.get_balance(hexa_address)
        return render_template('address.html', hexa_address=hexa_address, balance=weiBalance)
    return render_template('search_address.html')

# Template filters (Jinja2)
@app.template_filter('since')
def findSince(timestamp):
    """Convert the given timestamp into "%Y-%m-%d %H:%M:%S" string format
        And calculate the difference (in seconds)
        between the converted timestamp and the datetime.now()

        Return a string depending on the seconds value
    """
    return checkSeconds(fromTimestampToNow(timestamp))

@app.template_filter('fromHex')
def fromHexBytes(hex):
    """ Decode HeBytes into string
    """
    return hex.hex()

@app.template_filter('fromWei')
def fromHexBytes(Wei):
    """ Convert Wei into Ether
        Return O if Eth < 0.01 else
    """
    toEth = w3.fromWei(Wei, 'ether')
    return round(toEth, 4) if toEth >= 0.01 else 0


@app.template_filter('cutter')
def cutLongStr(longStr):
    """ Cut long string and return the first 9 chars + '...'
    """
    return longStr[:9]+ '...'

if __name__ == "__main__":
    """main func()"""
    app.run(host='0.0.0.0', port=5000, threaded=True)
