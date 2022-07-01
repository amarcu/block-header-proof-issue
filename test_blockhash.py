import math
import argparse
import json
import sys
import os
from pprint import pprint
from getpass import getpass

from web3 import Web3
from web3.logs import DISCARD
import requests
import rlp

from utils import normalize_bytes, normalize_address, normalize_int, decode_hex, to_0x_string
from state_proof import request_block_header, request_account_proof

ORACLE_CONTRACT_ADDRESS = '0xbfdF11DAB37cAFD02579614F4cE9CA8D5daD8BF0'

def main():
    parser = argparse.ArgumentParser(
        description="Patricia Merkle Trie Proof Generating Tool",
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-r", "--rpc",
        default="http://localhost:8545",
        help="URL of a full node RPC endpoint, e.g. http://localhost:8545")

    parser.add_argument("-b", "--block-number",
        help="Block number")

    args = parser.parse_args()
    w3 = Web3(Web3.HTTPProvider(args.rpc))

    (block_number, block_header) = generate_proof_data(
            rpc_endpoint=args.rpc,
            block_number=args.block_number,
            london_fork=int(args.block_number)>=12965000
        )

    header_blob = rlp.encode(block_header)
    computedHash = Web3.keccak(header_blob).hex()
    print(f"Computed hash    {computedHash}")

def generate_proof_data(
    rpc_endpoint,
    block_number,
    london_fork
):
    block_number = \
        block_number if block_number == "latest" or block_number == "earliest" \
        else hex(int(block_number))

    (block_number, block_header) = request_block_header(
        rpc_endpoint=rpc_endpoint,
        block_number=block_number,
        london_fork=london_fork
    )

    return (
        block_number,
        block_header
    )

if __name__ == "__main__":
    main()
    exit(0)