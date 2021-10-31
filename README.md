WatchYourHash - Ethereum Block Explorer v1
---
## About the project

Ethereum, like any **blockchain**, is an **open-source database** of information that is designed to be unhackable. Ether (ETH) is the cryptocurrency used to complete transactions on the blockchain.

[watchyourhash.me](https://www.watchyourhash.me) is a web application that allows you to **navigate** and **retrieve** informations in the Ethereum blockchain.
The application query the Ethereum blockchain via **Web3.py** using **Infura**, an Ethereum Node Provider.

## Usage

### Blocks

You can access all blocks by entering the height of the block in the search bar. You will be redirected to the block page, where you will have access to the main information of this block such as the address that mined it, the number of transactions registered in the block, the burned fees etc. 
You can also add to the search bar the /block/ page with the number of the block for example:

> https://watchyourhash.me/block/13521742

It will redirect you to the same page.
### Transactions

As for the blocks, you can access all transactions registered on the Ethereum blockchain. Just paste the hash in the search bar and you will be redirected to the transaction page.
You can also access it with the url:

> https://watchyourhash.me/transaction/0x56ba1efb2baa7467a9c5a525c9c0d2ab836ecfecf5c1d460fcb7e07523587d98

Note: Ethereum hosts on its chain many tokens that are part of the Ethereum ecosystem, and thus its transactions. Lapp allows you to see only Ether transactions. You cannot track other tokens for the moment.

### Address

Access the amount of Eth your address got and display the current value in USD
You can access it via the search bar or the url:

> https://watchyourhash.me/address/0x2daa35962a6d43eb54c48367b33d0b379c930e5e

## Built with

- Flask
- Infura
- Web3.py
- Blockchair API
- Bootstrap
- Materiel Design Bootstrap
- Nginx
- Gunicorn
- Metamask (JS)

## Getting started

To get a local copy up and running follow these simple example steps.

Installation:

1. Clone the repo
- git clone github.com/EtienneBrJ/Portfolio.git

2. Move to the project directory:
- cd Portfolio

3. Get a free API key at infura.com and change INFURA_API_KEY in config.py

4. Create a virtual env, start it and install the required modules with pip:
- python3 -m venv env
- source env/bin/activate
- pip install -r requirements.txt

5. Start the bash script flask_dev.sh, it will start the flask app in development mode:
- ./flask_dev.sh

6. Access it via your browser:
- http://0.0.0.0:5000

## Source

[Ethereum](https://ethereum.org/en/developers/docs/intro-to-ethereum/)<br>
[Web3.py Docs](https://web3py.readthedocs.io/en/stable/quickstart.html)<br>
[Infura](https://infura.io/)<br>
[Blockchair API Docs](https://blockchair.com/api/docs#link_M1)<br>
[Metamask Wallet](https://metamask.io/)

## Contributing

Feel free to contribute, it still has little bugs to fix :D

## Contact

[Etienne Brun](https://www.linkedin.com/in/etienne-brun-06187a205/)<br>Project Link : [watchyourhash](https://github.com/EtienneBrJ/Portfolio)