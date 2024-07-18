from web3 import Web3
# 连接到以太坊节点 - 这里使用的是本地节点
w3 = Web3(Web3.HTTPProvider('http://localhost:7545'))
# 确保与节点的连接
if not w3.is_connected():
    print("Failed to connect to Ethereum node")
    exit()
# 合约地址和ABI
contract_address = Web3.to_checksum_address("0x187fb261ea86f208640735bbfe9bd1d549be837f") # 替换为您的合约地址
contract_abi = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "downloader",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "downloadedData",
                "type": "string"
            }
        ],
        "name": "DataDownloaded",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "uploader",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "newData",
                "type": "string"
            }
        ],
        "name": "DataUploaded",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_licensee",
                "type": "address"
            }
        ],
        "name": "addLicensee",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_Householder",
                "type": "address"
            }
        ],
        "name": "addReceiver",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "downloadData",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "householders",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "licensees",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "storedData",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "newData",
                "type": "string"
            }
        ],
        "name": "uploadData",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "viewData",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]# 替换为您的合约ABI



# 设置账户
w3.eth.defaultAccount = '0x412cA3493A021e5e115e874Ce941021C59d7e308'  # 设置默认账户,owner地址
# 创建合约对象
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# 用户地址和私钥（请确保这是安全的环境，不要泄露您的私钥）
user_address = '0x075e25D53ab1136Afd356fc4363754b4559F1A42'
# 获取nonce
nonce_address = Web3.to_checksum_address('0x0f120e3b86d41ee600f32856ca76e9cd65342cec')
nonce = w3.eth.get_transaction_count(nonce_address)
# 获取owner地址
# owner_address = contract.functions.owner().call()
# print(f"The owner of the contract is: {owner_address}")
def authAgents(operator_address):
    # 调用函数授权新地址
    tx_hash = contract.functions.addAgent(user_address).transact({'from': operator_address})
    w3.eth.wait_for_transaction_receipt(tx_hash)

# 调用uploadData函数
def authSpenders(operator_address):
    # 调用函数授权新地址
    tx_hash = contract.functions.addAgent(user_address).transact({'from': operator_address})
    w3.eth.wait_for_transaction_receipt(tx_hash)

def callUploadDate(operator_address,data):
    # 调用上传数据的函数
    transaction_hash = contract.functions.uploadData(data).transact({'from':operator_address})
    w3.eth.wait_for_transaction_receipt(transaction_hash)


# # 发送交易
# upload_tx_hash = web3.eth.send_raw_transaction(signed_upload_tx.rawTransaction)
#
# # 等待交易被挖掘
# upload_tx_receipt = web3.eth.wait_for_transaction_receipt(upload_tx_hash)
# print(f"Upload Transaction Receipt: {upload_tx_receipt}")

# 调用downloadData函数
# download_data = contract.functions.downloadData().call()
# print(f"Downloaded Data: {download_data}")
def authRecievers(operator_address):
    # 调用函数授权新地址
    tx_hash = contract.functions.addAgent(user_address).transact({'from': operator_address})
    w3.eth.wait_for_transaction_receipt(tx_hash)

def callDownloaddata(operator_address):
    download_data = contract.functions.downloadData().call({'from': operator_address})
    print(f"download Data: {download_data}")
    return download_data


# 调用viewData函数
def callViewdata():
    view_data = contract.functions.viewData().call()
    print(f"Viewed Data: {view_data}")
    return view_data






