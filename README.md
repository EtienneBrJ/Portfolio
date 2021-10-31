WatchYourHash - Ethereum Block Explorer v1 ([watchyourhash.me](https://watchyourhash.me))
---
## Portfolio

The Portfolio project is the end of year project at Holberton. It is a one month project where we are completely independent. I chose to explore the topic of blockchain because I was interested in it before I knew how to code.I had a lot of fun doing this project and I wish I had more time to explore the subject more deeply.

### About the project

Ethereum, like any **blockchain**, is an **open-source database** of information that is designed to be unhackable. Ether (ETH) is the cryptocurrency used to complete transactions on the blockchain.

[watchyourhash.me](https://www.watchyourhash.me) is a web application that allows you to **navigate** and **retrieve** informations in the Ethereum blockchain.
The application query the Ethereum blockchain via **Web3.py** using **Infura**, an Ethereum Node Provider.

## Usage
#### Blocks

You can access all blocks by entering the height of the block in the search bar. You will be redirected to the block page, where you will have access to the main information of this block such as the address that mined it, the number of transactions registered in the block, the burned fees etc.
You can also add to the url the /block/ page with the number of the block for example:

>https://watchyourhash.me/block/13521742

It will redirect you to the same page.
#### Transactions

As for the blocks, you can access all transactions registered on the Ethereum blockchain. Just paste the hash in the search bar and you will be redirected to the transaction page.
You can also access it with the url:

>https://watchyourhash.me/transaction/0x56ba1efb2baa7467a9c5a525c9c0d2ab836ecfecf5c1d460fcb7e07523587d98

Note: Ethereum hosts on its chain many tokens that are part of the his ecosystem, and its transactions. The app allows you to see only Ether transactions. You cannot track other tokens for the moment.

#### Address

Access the amount of Eth your address got and display the current value in USD.
You can access it via the search bar or the url:

>https://watchyourhash.me/address/0x2daa35962a6d43eb54c48367b33d0b379c930e5e

#### Metamask

MetaMask is a software cryptocurrency wallet used to interact with the Ethereum blockchain. You can connect your wallet to the site but for the moment the transaction feature is not available.


## Getting started

To get a local copy up and running follow these simple example steps.

Installation:

1. Clone the repo

        git clone github.com/EtienneBrJ/Portfolio.git


2. Move to the project directory:
        
        cd Portfolio

3. Get a free API key at infura.com and add it to INFURA_API_KEY in config.py

4. Create a virtual env, start it and install the required modules with pip:

        python3 -m venv env
        source env/bin/activate
        pip install -r requirements.txt

5. Start the bash script flask_dev.sh, it will start the flask app in development mode:

        ./flask_dev.sh

6. Access it via your browser:

        http://0.0.0.0:5000

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

## Contributing

Feel free to contribute

## Contact

[Linkedin](https://www.linkedin.com/in/etienne-brun-06187a205/)<br>[Twitter](https://twitter.com/read2696)<br>etiennebrxv@gmail.com
## Deployed app

[Landing page](https://EtienneBrJ.github.io)<br>[Web app](https://watchyourhash.me)


## Source

[Ethereum](https://ethereum.org/en/developers/docs/intro-to-ethereum/) - [Web3.py Docs](https://web3py.readthedocs.io/en/stable/quickstart.html) - [Infura](https://infura.io/) - [Blockchair API Docs](https://blockchair.com/api/docs#link_M1) - [Metamask Wallet](https://metamask.io/)