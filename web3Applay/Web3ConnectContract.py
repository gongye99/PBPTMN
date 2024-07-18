from web3 import Web3
import time
start_time = time.time()
# 连接到本地以太坊节点（例如 Ganache）
w3 = Web3(Web3.HTTPProvider('http://localhost:7545'))

# 合约地址和 ABI（需要根据你的合约部署情况进行修改）
contract_address = "0x3FB4F145bb5Be33EbE7b544ca5B22Bf54aAAE43C"
contract_abi = [
{
		"inputs": [
			{
				"internalType": "address",
				"name": "_agent",
				"type": "address"
			}
		],
		"name": "addAgent",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_receiver",
				"type": "address"
			}
		],
		"name": "addReceiver",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_spender",
				"type": "address"
			}
		],
		"name": "addSpender",
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
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "agents",
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
				"name": "_address",
				"type": "address"
			}
		],
		"name": "isAgent",
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
				"name": "_address",
				"type": "address"
			}
		],
		"name": "isReceiver",
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
				"name": "_address",
				"type": "address"
			}
		],
		"name": "isSpender",
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
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "receivers",
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
		"name": "spenders",
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
]

# 使用合约 ABI 和地址创建合约对象
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# 调用上传数据的函数
transaction_hash = contract.functions.uploadData("312").transact({'from': '0x412cA3493A021e5e115e874Ce941021C59d7e308'})
w3.eth.wait_for_transaction_receipt(transaction_hash)

# 调用下载数据的函数
downloaded_data = contract.functions.downloadData().call({'from': '0x412cA3493A021e5e115e874Ce941021C59d7e308'})
print("Downloaded Data:", downloaded_data)

end_time = time.time()
run_time = end_time - start_time
print(f"程序运行时间：{run_time} 秒")