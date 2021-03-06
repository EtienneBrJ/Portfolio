#!/usr/bin/python3
""" Module regrouping all the main functions
"""
import config
import json
import requests
from web3 import Web3
from flask import request, flash, redirect
from eth_typing.encoding import HexStr


ws_provider = Web3.WebsocketProvider(config.MAINNET_WSS)
w3 = Web3(ws_provider)


def getlatestBlocks(n):
    """ Put in a list (append: add at the end of the list)
        the block_info of the n last blocks
    """
    last_blocks = []
    for number in range(w3.eth.block_number, w3.eth.block_number - n, -1):
        try:
            last_blocks.append(w3.eth.get_block(number))
        except:
            pass
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
            pass
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


def getEthInfosFromBC():
    """ Use Blockchair API to get some infos on Eth
    """
    req = requests.get('https://api.blockchair.com/ethereum/stats')
    text_response = json.loads(req.text)
    data = text_response.get('data')
    return data


def getAllTxsFees(nBlock):
    """ Call web3 to get all txs fees of a block
    """
    count = 0
    block = w3.eth.get_block(nBlock)
    for i in range(len(block.transactions)):
        tx = w3.eth.get_transaction(block.transactions[i])
        receipt = w3.eth.get_transaction_receipt(block.transactions[i])
        count += receipt.gasUsed * tx.gasPrice
    # Convert total txs_fees in wei to Eth
    # Return the txs_fees of nBlock
    return count / 1000000000000000000


def paginateBlocks(n, block_number=None):
    """ Paginate next n blocks
        Return a list of block informations
    """
    last_blocks = []
    if block_number:
        for number in range(block_number, block_number - n, -1):
            last_blocks.append(w3.eth.get_block(number))
        return last_blocks


def checkSeconds(seconds, timestamp):
    """ Return a string depending on the value of seconds
        If the block is mined since one hour ago, return timestamp
    """
    if 3600 > seconds > 60:
        minute = int(seconds / 60)
        if minute == 1:
            return '{} minute ago'.format(minute)
        return '{} minutes ago'.format(minute)
    else:
        return 'Since {} sec'.format(seconds)
