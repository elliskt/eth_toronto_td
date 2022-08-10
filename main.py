# -*- coding: utf-8 -*-
# author: Ellis
import mimetypes
import os
import utils
import flask
from flask import request
from flask_cors import *
import pymongo
import argparse
import warnings
from ankr import AnkrWeb3
from ankr.types import Blockchain


warnings.filterwarnings('ignore')
# --- setting argparser ---
parser = argparse.ArgumentParser(prog='Flask API',
                                 usage='[optionals] Example: python3 main.py')
parser.add_argument('--host', metavar='', type=str, default='localhost', help='Input localhost or host X.X.X.X')
args, unknown = parser.parse_known_args()
# --- connect to db ---
client = pymongo.MongoClient('127.0.0.1', 27017)
ting_db = client.eth_toronto_collection
col_collections = ting_db.collections
HOST = '0.0.0.0' if args.host == 'localhost' else args.host.lower()
# --- flask server ----
server = flask.Flask(__name__, static_folder='database')
CORS(server, supports_credetials=True)
# --- ankr ---
ankr_w3 = AnkrWeb3()


@server.route("/retrieve_personal_collections", methods=['POST'])
def retrieve_personal_collections():
    data = request.get_json()
    user_address = data['user_address']
    user_address = utils.checkSumAddress(user_address)
    # --- by using ANKR API to get nft information
    nfts = ankr_w3.nft.get_nfts(
        blockchain=[Blockchain.ETH],
        wallet_address=user_address,
    )
    nfts = list(nfts)

    utils.getCollections(user_address, nfts)


@server.route("/get_collections", methods=['GET'])
def get_collections():
    data = request.get_json()
    user_address = data['user_address']
    user_address = utils.checkSumAddress(user_address)
    col = col_collections.find({'owner': user_address})
    collections = dict()
    collections['data'] = []
    for i in col:
        collections['data'].append(i)

    return collections


@server.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


if __name__ == '__main__':
    server.run(host=HOST, port=8800, debug=True, threaded=True)
