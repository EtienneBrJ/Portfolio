#!/usr/bin/python3
""" Flask application
"""
import config
from web3 import Web3
from datetime import datetime
from flask import Flask, render_template, request, redirect
from funcs import *

ws_provider = Web3.WebsocketProvider(config.MAINNET_WSS)
w3 = Web3(ws_provider)


app = Flask(__name__)

app.jinja_env.globals.update(fromBC=getEthInfosFromBC)


# Inbuilt function handling 404 error
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

# Routes


@app.route('/', methods=["POST", "GET"])
def index():
    """ Index page
        Display the 10 latest blocks
        Display the 10 lasts transactions of the last block
    """
    if request.method == 'POST':
        search_url = checkIncomingReq(request.form['search'])
        if search_url:
            return redirect(search_url)
    return render_template('index.html', last_blocks=getlatestBlocks(10),
                           txs=getlatestTxn(10), miners=config.dict_miners)


@app.route('/blocks/', methods=["POST", "GET"])
@app.route('/block/<int:block_number>', methods=["POST", "GET"])
def block(block_number=None):
    """ Handle block/s template
        where block_number is the Height of the block in the chain
    """
    if request.method == 'POST':
        search_url = checkIncomingReq(request.form['search'])
        if search_url:
            return redirect(search_url)
    if block_number:
        info_block = w3.eth.get_block(block_number)
        return render_template('block.html', last_block=info_block,
                               miners=config.dict_miners)
    return render_template('blocks.html', last_blocks=getlatestBlocks(10),
                           miners=config.dict_miners)


@app.route('/blocks/<int:block_number>/paginate', methods=["POST", "GET"])
def paginate(block_number=None):
    """ Handle pagination for blocks template
        where block_number is the Height of the block in the chain

        Display 10 blocks per page
    """
    if request.method == 'POST':
        search_url = checkIncomingReq(request.form['search'])
        if search_url:
            return redirect(search_url)
    if block_number:
        return render_template('blocks.html',
                               last_blocks=paginateBlocks(10, block_number),
                               miners=config.dict_miners)


@app.route('/block/<int:block_number>/transactions/<int:page>',
           methods=["POST", "GET"])
def paginate_transaction(block_number=None, page=None):
    """ Handle pagination for transactions template
        where block_number is the Height of the block in the chain

        Display 15 txs per_page
    """
    if request.method == 'POST':
        search_url = checkIncomingReq(request.form['search'])
        if search_url:
            return redirect(search_url)
    if block_number:
        txs = []
        per_page = 15
        block = w3.eth.get_block(block_number)
        for i in range(per_page * (page-1), per_page * page):
            try:
                txs.append(w3.eth.get_transaction(block.transactions[i]))
            except:
                pass
        return render_template('transactions.html', txs=txs,
                               block=block, page=page)


@app.route('/transactions/', methods=["POST", "GET"])
@app.route('/transaction/<hash>', methods=["POST", "GET"])
def transaction(hash=None):
    """ Handle transaction/s template
        where hash is the hash of the transaction
    """
    if request.method == 'POST':
        search_url = checkIncomingReq(request.form['search'])
        if search_url:
            return redirect(search_url)
    if hash:
        tx = w3.eth.get_transaction(hash)
        receipt = w3.eth.get_transaction_receipt(hash)
        txBlock = w3.eth.get_block(tx.blockHash)
        return render_template('transaction.html', tx=tx, txBlock=txBlock,
                               receipt=receipt)
    return render_template('transactions.html', txs=getlatestTxn(10),
                           last_block=w3.eth.get_block('latest'))


@app.route('/address/', methods=["POST", "GET"])
@app.route('/address/<hexa_address>', methods=["POST", "GET"])
def address(hexa_address=None):
    """ Handle address template
        where hexa_address is the address
    """
    if request.method == 'POST':
        search_url = checkIncomingReq(request.form['search'])
        if search_url:
            return redirect(search_url)
    if hexa_address:
        weiBalance = w3.eth.get_balance(hexa_address)
        return render_template('address.html', hexa_address=hexa_address,
                               balance=weiBalance, miners=config.dict_miners)
    return render_template('layout.html')


@app.template_filter('since')
def findSince(timestamp):
    """ Convert the given timestamp into "%Y-%m-%d %H:%M:%S" string format
        And calculate the difference (in seconds)
        between the converted timestamp and the datetime.now()

        if the block has been mined for more than an hour
            return the block timestamp convert to datetime
        else
        Return a string depending on seconds (see checkSeconds)
    """
    strDate = str(datetime.fromtimestamp(timestamp))
    blockDate = datetime.strptime(strDate, "%Y-%m-%d %H:%M:%S")
    seconds = (datetime.now()-blockDate).seconds
    if seconds > 3600:
        return blockDate
    return checkSeconds(seconds, timestamp)


@app.template_filter('fromHex')
def fromHexBytes(hex):
    """ Decode HeBytes into string
    """
    return hex.hex()


@app.template_filter('fromWeiRounded')
def fromWei(Wei, nRound):
    """ Convert Wei into Ether
        Return O if Eth < 0.01 else
    """
    if type(Wei) is str:
        Wei = int(Wei)
    toEth = w3.fromWei(Wei, 'ether')
    return round(toEth, nRound)


@app.template_filter('cutter')
def cutLongStr(longStr):
    """ Cut long string and return the first 9 chars + '...'
    """
    return (longStr[:6] + '..' + longStr[-4:]).lower()


@app.template_filter('comma')
def commaInt(n):
    """ Format int:
        Put a comma after each 3 digits starting from the right
    """
    return '{:,}'.format(n)


@app.template_filter('toGwei')
def weiToGwei(n):
    """ Return an int that display baseFeePerGas in Gwei
    """
    # Convert form wei to Gwei
    return int(n / 1000000000)


@app.template_filter('burntFees')
def calculateBurntFees(a, b):
    """ Multiply gasUsed and baseFeePerGas of a block to find the Burnt fees
    Return the fees rounded at 4 decimals
    """
    n = a * b
    # Convert from wei to Eth
    e = n / 1000000000000000000
    return round(e, 4)


@app.template_filter('getTxFees')
def getTxFees(gasPrice, hash):
    """ Call web3 to get the receipt of a transaction to
        return the tx fees of this transaction
    """
    try:
        receipt = w3.eth.get_transaction_receipt(hash)
    except:
        pass
    tx_fees = (gasPrice / 1000000000000000000) * receipt.gasUsed
    return round(tx_fees, 6)


@app.template_filter('getReward')
def getReward(block_number, ethBurnt):
    """ Calculate the Reward of a block using his block_number
    """
    allTxsFees = getAllTxsFees(block_number)
    return 2 + (allTxsFees - ethBurnt)


if __name__ == "__main__":
    """ Starting the app... """
    app.run(host='0.0.0.0', port=5000, threaded=True)
    