import json
from web3 import Web3
import pymongo
import cv2
from PIL import Image
import os
import requests
import web3

client = pymongo.MongoClient('127.0.0.1', 27017)
ting_db = client.eth_toronto_collection
col_collections = ting_db.collections
def checkSumAddress(addr):
    try:
        return(Web3.toChecksumAddress(addr))
    except TypeError as e:
        print('[ERROR] address format error ---> {}.'.format(addr))


def getCollections(acc, nfts):
    acc = checkSumAddress(acc)
    # ---
    for nft in nfts:
        # get data from ANKR
        if nft.token_id:
            col_collections.insert_one({'owner': acc,
                                'contract_address': nft.contract_address,
                                'image_url': nft.image_url,
                                'token_url': nft.token_url,
                                'c_name': nft.collection_name,
                                'symbol': nft.symbol,
                                'traits': nft.traits,
                                'contract_type': nft.contract_type
                             })


