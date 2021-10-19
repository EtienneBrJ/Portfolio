#!/usr/bin/python3
""" Application file

    Defining routes of the web application
"""
import config
from web3 import Web3
from filters_builder import checkSeconds, fromTimestampToNow
from flask import Flask, render_template, request, redirect
from funcs import getEthInfos, getlatestBlocks, getlatestTxn, checkIncomingReq, getAllTxsFees, paginateBlocks
from etherscan import callEtherScanAPI, getEtherInCirculation, getEtherLastPrice, getTotalEthNodes


ws_provider = Web3.WebsocketProvider(config.MAINNET_WSS)
w3 = Web3(ws_provider)


app = Flask(__name__)

app.jinja_env.globals.update(getEtherInCirculation=getEtherInCirculation)
app.jinja_env.globals.update(getTotalEthNodes=getTotalEthNodes)
app.jinja_env.globals.update(getEtherLastPrice=getEtherLastPrice)
app.jinja_env.globals.update(callEtherScanAPI=callEtherScanAPI)



# Inbuilt function handling 404 error
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

# Routes
@app.route('/', methods=["POST", "GET"])
def index():
    """ Home page, if request.method is POST, call the func 
    """
    if request.method == 'POST':
        search_url = checkIncomingReq(request.form['search'])
        if search_url:
            return redirect(search_url)
    return render_template('index.html', last_blocks=getlatestBlocks(10),
                            last_txn=getlatestTxn(10), miners=config.dict_miners,
                            price=getEthInfos())

@app.route('/blocks/', methods=["POST", "GET"])
@app.route('/block/<int:block_number>', methods=["POST", "GET"])
def block(block_number=None):
    """ Block page """
    if request.method == 'POST':
        search_url = checkIncomingReq(request.form['search'])
        if search_url:
            return redirect(search_url)
    if block_number:
        info_block = w3.eth.get_block(block_number)
        return render_template('block.html', last_block=info_block, miners=config.dict_miners, price=getEthInfos())
    return render_template('blocks.html', last_blocks=getlatestBlocks(10), miners=config.dict_miners, price=getEthInfos())

@app.route('/blocks/<int:block_number>/paginate', methods=["POST", "GET"])
def paginate(block_number=None):
    """ Pagination for blocks """
    if request.method == 'POST':
        search_url = checkIncomingReq(request.form['search'])
        if search_url:
            return redirect(search_url)
    if block_number:
        return render_template('blocks.html', last_blocks=paginateBlocks(10, block_number), miners=config.dict_miners, price=getEthInfos())

@app.route('/transactions/', methods=["POST", "GET"])
@app.route('/transaction/<hash>', methods=["POST", "GET"])
def transaction(hash=None):
    """ Tx page """
    if request.method == 'POST':
        search_url = checkIncomingReq(request.form['search'])
        if search_url:
            return redirect(search_url)
    if hash:
        tx = w3.eth.get_transaction(hash)
        receipt = w3.eth.get_transaction_receipt(hash)
        txBlock = w3.eth.get_block(tx.blockHash)
        return render_template('transaction.html', tx=tx, txBlock=txBlock , receipt=receipt, price=getEthInfos())
    return render_template('transactions.html', last_txn=getlatestTxn(10), last_block=w3.eth.get_block('latest'), price=getEthInfos())
    


@app.route('/address/', methods=["POST", "GET"])
@app.route('/address/<hexa_address>', methods=["POST", "GET"])
def address(hexa_address=None):
    """ Address page """
    if request.method == 'POST':
        search_url = checkIncomingReq(request.form['search'])
        if search_url:
            return redirect(search_url)
    if hexa_address:
        weiBalance = w3.eth.get_balance(hexa_address)
        return render_template('address.html', hexa_address=hexa_address, balance=weiBalance, price=getEthInfos())
    return render_template('layout.html', price=getEthInfos())

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

@app.template_filter('fromWeiRounded')
def fromWei(Wei, nRound):
    """ Convert Wei into Ether
        Return O if Eth < 0.01 else
    """
    toEth = w3.fromWei(Wei, 'ether')
    return round(toEth, nRound)


@app.template_filter('cutter')
def cutLongStr(longStr):
    """ Cut long string and return the first 9 chars + '...'
    """
    return longStr[:9]+ '...'

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
    receipt = w3.eth.get_transaction_receipt(hash)
    tx_fees = (gasPrice / 1000000000000000000)* receipt.gasUsed
    return round(tx_fees, 6)

@app.template_filter('getReward')
def getReward(block_number, ethBurnt):
    """ Calculate the Reward of a block using his block_number 
    """
    allTxsFees = getAllTxsFees(block_number)
    return 2 + (allTxsFees - ethBurnt)


if __name__ == "__main__":
    """main func()"""
    app.run(host='0.0.0.0', port=5000, threaded=True)
