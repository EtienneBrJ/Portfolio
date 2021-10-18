import config, requests, json

def getEtherInCirculation():
    """ Call Etherscan API to get the current Ether in circulation 
        Get the value in Wei, conversion to Eth and return
    """
    supplyReq = requests.get('https://api.etherscan.io/api?module=stats&action=ethsupply&apikey=' + config.ETHERSCAN_KEY)
    supply = json.loads(supplyReq.text).get('result')
    supplyInEth = int(supply) / 1000000000000000000
    return supplyInEth

def getTotalEthNodes():
    """ Call Etherscan API to get the  total number of discoverable Ethereum nodes and
        Return it
    """
    totalNodesReq = requests.get('https://api.etherscan.io/api?module=stats&action=nodecount&apikey=' + config.ETHERSCAN_KEY)
    totalNodes = json.loads(totalNodesReq.text).get('result').get('TotalNodeCount')
    return totalNodes

def getEtherLastPrice():
    """ Call Etherscan API and
        Return a dict with Eth or BTC as key
        and its associated USD value 
    """
    priceReq = requests.get('https://api.etherscan.io/api?module=stats&action=ethprice&apikey=' + config.ETHERSCAN_KEY)
    result = json.loads(priceReq.text).get('result')
    eth_btc = result.get('ethbtc')
    xBtc = 1 / float(eth_btc)
    priceEth = result.get('ethusd')
    priceBtc = float(priceEth) * xBtc
    priceBtc = round(priceBtc, 1)
    return dict(ethereum=priceEth, bitcoin='{}'.format(priceBtc))

def callEtherScanAPI():
    """ Pour renvoyer un dic avec toutes les infos
        Pour l'instant, stock juste le html d'avant
        Prends trop de temps pour faire les requetes.
        Doit autmatiser une requete toutes les 15s que je stock dans un dic et que je passe au template
    """
    htmlApiCall = "<p class='m-2 h6'>Ether in circulation : {{ getEtherInCirculation() | int | comma }}</p>\
        <p class='m-2 h6'>Total number of Ethereum nodes : {{ getTotalEthNodes() | int | comma }}</p>\
        <p class='m-2 h6'>Ethereum Price : {{ getEtherLastPrice().ethereum | int | comma }} $ </p>\
        <p class='m-2 h6'>Bitcoin Price : {{ getEtherLastPrice().bitcoin | int | comma }} $ </p>"
    return htmlApiCall
