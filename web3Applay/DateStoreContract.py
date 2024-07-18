from web3 import Web3
import time
# 连接到以太坊节点 - 这里使用的是本地节点
w3 = Web3(Web3.HTTPProvider('http://localhost:7545'))
# 确保与节点的连接
if not w3.is_connected():
    print("Failed to connect to Ethereum node")
    exit()
# 合约地址和ABI
contract_address = Web3.to_checksum_address("0x558bd2492a658712f90e027b706c6e8952667bba") # 替换为您的合约地址
contract_abi =[
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
w3.eth.defaultAccount = '0xfe0ff29e1471afba16b14be834b89f754e5307ab'  # 设置默认账户,owner地址
# 创建合约对象
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# 用户地址和私钥（请确保这是安全的环境，不要泄露您的私钥）
user_address = '0x075e25D53ab1136Afd356fc4363754b4559F1A42'
# 获取nonce
nonce_address = Web3.to_checksum_address('0x0f120e3b86d41ee600f32856ca76e9cd65342cec')
nonce = w3.eth.get_transaction_count(nonce_address)
# 获取owner地址
owner_address = contract.functions.owner().call()
# print(f"The owner of the contract is: {owner_address}")
def authAgents(operator_address):
	# 调用函数授权新地址
	tx_hash = contract.functions.addAgent(user_address).transact({'from': operator_address})
	w3.eth.wait_for_transaction_receipt(tx_hash)

# 调用uploadData函数
def authSpenders(operator_address,user_address):
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
def authRecievers(operator_address,user_address):
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

if __name__ == '__main__':
	# start_time = time.time()
	authSpenders(owner_address,"0x85805Ae2052EEa616db6c1A08e19d326Dac756B6")
	callUploadDate("0x85805Ae2052EEa616db6c1A08e19d326Dac756B6","s4M9VigeyOGpdooUuda7Hcx/Em3Sj1FmB9LeaEI5UviUpRavLZyLWAtsL33Efbha0GN0ACDtbn4=")
	# end_time = time.time()
	# run_time = end_time - start_time
	# print(f"程序运行时间：{run_time} 秒")
	start_time = time.time()
	authRecievers(owner_address,"0xdDb627D116FCde7F60261b9cd67C2a153247C3A9")
	callDownloaddata("0xdDb627D116FCde7F60261b9cd67C2a153247C3A9")
	end_time = time.time()
	run_time = end_time - start_time
	print(f"程序运行时间：{run_time} 秒")




