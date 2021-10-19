#!/usr/bin/python3
""" Module regrouping all the main functions
"""
from logging import error
import config
from web3 import Web3
from flask import request, flash, redirect
from eth_typing.encoding import HexStr
from pycoingecko import CoinGeckoAPI


ws_provider = Web3.WebsocketProvider(config.MAINNET_WSS)
w3 = Web3(ws_provider)


def getlatestBlocks(n):
    """ Put in a list (append: add at the end of the list)
        the block_info of the n last blocks
    """
    last_blocks = []
    for number in range(w3.eth.block_number, w3.eth.block_number -n, -1):
        last_blocks.append(w3.eth.get_block(number))
    return last_blocks

def paginateBlock(n, block_number=None):
    """ Paginate
        Return a list of block informations
    """
    last_blocks = []
    if block_number:
        for number in range(block_number -1, block_number -(n+1), -1):
            last_blocks.append(w3.eth.get_block(number))
        return last_blocks


def getlatestTxn(n):
    """ Put in a list (append: add at the end of the list)
        the nth transactions informations of the last mined block
    """
    last_txn = []
    for idx in range(n):
        try:
            last_txn.append(w3.eth.get_transaction_by_block('latest', idx))
        except:
            last_txn.append(w3.eth.get_transaction_by_block(w3.eth.get_block_number() - 1, idx))
    return last_txn

def checkIfTx(inputData):
    """ Call a web3 func to check if the response exist
    If it is, return the redirection path
    """
    tx = None
    try:
        tx = w3.eth.get_transaction(inputData)
    except:
        pass
    if tx:
        return '/transaction/{}'.format(inputData)

def checkIfAddr(inputData):
    """ Call a web3 func to check if the response exist
    If it is, return the redirection path
    """
    addr = None
    try:
        # convert the input to checksum address coz of web3 isAddress func
        addr = w3.toChecksumAddress(inputData)
        w3.isAddress(addr)
    except:
        pass
    if addr:
        return '/address/{}'.format(addr)

def checkIfBlockN(inputData):
    """ Call a web3 func to check if the response exist
        If it is, return the redirection path
    """
    block = None
    try:
        inputData = int(request.form['search'])
        block = w3.eth.get_block(inputData)
    except:
        pass
    if block:
        return '/block/{}'.format(inputData)
    
def checkIncomingReq(input_data):
    """ Check for the incoming request.
        Post request from the FORM, return:
    
        Call a func to check if its a tx (/transaction/<hash>)
        Call a func to check if its a balance (/balance/<address>)
        Call a func to check if its a block (/block/<int:block_number>)
    """
    inputData = HexStr(input_data)
    try:
        tx = checkIfTx(inputData)
    except:
        flash('Invalid input')
        redirect('/')
    if tx:
        return tx
    try:
        addr = checkIfAddr(inputData)
    except:
        flash('Invalid input')
        redirect('/')
    if addr:
        return addr
    try:
        block = checkIfBlockN(inputData)
    except:
        flash('Invalid input')
        redirect('/')
    if block:
        return block

def getEthInfos():
    """ Use Coick Gecko API to get some infos on Eth """

    cg = CoinGeckoAPI()
    eth_infos = cg.get_price(ids='ethereum', vs_currencies='usd', include_market_cap=True, include_24hr_vol=True)
    return eth_infos

def getAllTxsFees(nBlock):
    """ Call web3 to get the all txs fees of a block
    """
    count = 0
    block = w3.eth.get_block(nBlock)
    for i in range(len(block.transactions)):
        tx = w3.eth.get_transaction(block.transactions[i])
        receipt = w3.eth.get_transaction_receipt(block.transactions[i])
        count += receipt.gasUsed * tx.gasPrice
    #Convert total txs_fees in wei to Eth
    # Return the txs_fees of nBlock
    return count / 1000000000000000000
