#!/usr/bin/python3
""" Module regrouping all the main functions
"""
import config
from web3 import Web3

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
