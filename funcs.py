#!/usr/bin/python3
""" Module regrouping all the main functions
"""
import config
from web3 import Web3
from flask import redirect, request
from eth_typing.encoding import HexStr



ws_provider = Web3.WebsocketProvider(config.MAINNET_WSS)
w3 = Web3(ws_provider)


def getlatestBlocks(n=5):
    """ Put in a list (append: add at the end of the list)
        the block_info of the n last blocks
    """
    last_blocks = []
    for number in range(w3.eth.block_number, w3.eth.block_number -n, -1):
        last_blocks.append(w3.eth.get_block(number))
    return last_blocks


def getlatestTxn(n=5):
    """ Put in a list (append: add at the end of the list)
        the nth transactions informations of the last mined block
    """
    last_txn = []
    for idx in range(n):
        last_txn.append(w3.eth.get_transaction_by_block('latest', idx))
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
        addr = w3.eth.get_balance(inputData)
    except:
        pass
    if addr:
        return '/address/{}'.format(inputData)

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
    tx = checkIfTx(inputData)
    if tx:
        return tx
    addr = checkIfAddr(inputData)
    if addr:
        return addr
    block = checkIfBlockN(inputData)
    if block:
        return block



