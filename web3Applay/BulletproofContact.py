from web3 import Web3
import time
# 连接到以太坊节点 - 这里使用的是本地节点
w3 = Web3(Web3.HTTPProvider('http://localhost:7545'))
# 确保与节点的连接
if not w3.is_connected():
    print("Failed to connect to Ethereum node")
    exit()
# 合约地址和ABI
contract_address = Web3.to_checksum_address("0x2ec42534f95f203a6169649bcb7d4303fe0552bb") # 替换为您的合约地址
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
w3.eth.defaultAccount = '0xc3237b3415e1e460d4977b9fdc4a25fe15dcd04e'  # 设置默认账户,owner地址
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
def authAgents(operator_address,user_address):
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
	print(transaction_hash)
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
	proof=""" {'taux': 57454113276137396908569118747587079754098305329010379011976515423894164180330, 'mu': 106278416677539601615183690970848586532625458170900136989471469289547978185345, 't_hat': 8195561837573824355519802335916255916337986557959512644703324460774559457456, 'T1': X: 0x2601d8a01b6c6a3d2844ce7df92ae4a8f8e913c46d978ec8617c54e8fe13624e
Y: 0x79070b284dc4488a02f66b26563c9799da813bc2b9dd77ef9471cb96194ebaee
(On curve <secp256k1>), 'T2': X: 0x78bdd4577f48dc1891d5df3af0019ba1eeb40723017b862bc662e86463ce01fe
Y: 0x93b5fe7b57d3b2afa362cfdc86c867881960df0f26cc047df3499e719e1e749a
(On curve <secp256k1>), 'A': X: 0x1d60521ca267e9a46650f6f9345b4345dc1de20d259daad28a9c3f0e5754e9e5
Y: 0xb6683a166c88794cabc26c0694f15c6b23dac9b8d66baf0fd4fd68b85403d432
(On curve <secp256k1>), 'S': X: 0x1ec01667f62304378316aff00ea3f3ca723bd58e4696d7271bc6f93025f2ed0
Y: 0xd41eb7e40439ca9ab5d1ddc43646056c1c7740b709aaf5ee60d17b8e86b4bd29
(On curve <secp256k1>), 'innerProof': {'u_new': X: 0x20d1917d800b193666df96107205f8827d6473e3e1a10014bd80fa99d4337935
Y: 0xf7a71625e2b5bed96342426ade46ca5765bab6a0eebea3ba44780acbb62b838a
(On curve <secp256k1>), 'P_new': X: 0x7180281b2734f5516ab42f4dd1ec6c5c2e6d7197bca13bd0290836cd255b0c06
Y: 0xb8b9d8a98a0521338be8e9459da8820dbac73544f13a874360cd206e3da22fb4
(On curve <secp256k1>), 'proof2': {'a': 71311360884313724691987597491168029990402984128321867953621173733940347899417, 'b': 108043934864494154567108594523648096662955644702846675321304313523399172643286, 'xs': [102437727689472717218034429997928411619204248827486506518045714996553383310500, 41674164337147927330440137379610450482505736205408301189718002460258369534204, 1002117397317998168965696119385592072137002072769169876704283517388935074918, 79282880017265713771205160622893684972270928428719839148285958239820850397596], 'Ls': [X: 0xbb401f4074f5ae111027409fc756288c43369a3647eca856dd065a899ffa323a
Y: 0x3207bc7917e702cb931172600511e054a0832a52cee3c79bbc972c29cdbf6300
(On curve <secp256k1>), X: 0x3703adb6bc26d559f4a806aa08d173b98d151e0dff18affc2dd9b1fb3ba4eeed
Y: 0x8ad28430e3b6ad7263f22ddb63928ae81352b1bd1fba5aba68af35fdd95c5dd3
(On curve <secp256k1>), X: 0x75c5875420ad298c65fe11905b95993d2d65f2a650bb686ac98f69b6f69f3266
Y: 0x4a8166cb375695edb557a6df436d2c9407d7bc894b7baf4b6aa4fc61023b6ec9
(On curve <secp256k1>), X: 0xe473e994d5cb46af876736aae299e6f0940a03783e73f6161ebab4180d64c8a4
Y: 0x4e79ea378e9f73f3797759b896a41ad6d243794dbefba042a8a68fe6c260fd5d
(On curve <secp256k1>)], 'Rs': [X: 0xaa4cd568ea5ff5560c0361595c6a1e1f03b8741b94e4f6da43cd15bfd92ddc6d
Y: 0x82f8d04fd5d98855143500dfed0ae4d3597961cafd80214f78c872a7042d9caa
(On curve <secp256k1>), X: 0x86e46dfaaf761821b5a55710aa40c6a5368b3e78ea981cdf4f59332505e92eba
Y: 0x3179402d127451a1a8b6fcea0c8b1a2007de8229cc6b2bc6779a00854316c380
(On curve <secp256k1>), X: 0x8582df71bffcc7c614200f66bee3c6019b9b3d08e6812d39856267d74b5c0ce5
Y: 0x84d2822513000cba9f56522e57f521f6fa6a161f7eb98b622ba10ae80c6a6f0e
(On curve <secp256k1>), X: 0x6bfde79068e5d217efb46e85423acddbd0f065dcbedc349e6af26f185d69eda4
Y: 0xd686d5b9f950521f02e102c4ae268e5c59a917ac9f8ee03096fca908c948110c
(On curve <secp256k1>)], 'transcript': b'&&48232765580321784006667845622477657312754389262271342073231045816593267889580&ArtAH0B09a4RECdAn8dWKIxDNpo2R+yoVt0GWomf+jI6&AqpM1WjqX/VWDANhWVxqHh8DuHQblOT22kPNFb/ZLdxt&102437727689472717218034429997928411619204248827486506518045714996553383310500&AzcDrba8JtVZ9KgGqgjRc7mNFR4N/xiv/C3Zsfs7pO7t&AobkbfqvdhghtaVXEKpAxqU2iz546pgc309ZMyUF6S66&41674164337147927330440137379610450482505736205408301189718002460258369534204&A3XFh1QgrSmMZf4RkFuVmT0tZfKmULtoasmPabb2nzJm&AoWC33G//MfGFCAPZr7jxgGbmz0I5oEtOYViZ9dLXAzl&1002117397317998168965696119385592072137002072769169876704283517388935074918&A+Rz6ZTVy0avh2c2quKZ5vCUCgN4PnP2Fh66tBgNZMik&Amv955Bo5dIX77RuhUI6zdvQ8GXcvtw0nmrybxhdae2k&79282880017265713771205160622893684972270928428719839148285958239820850397596&', 'start_transcript': 3}, 'transcript': b'&48232765580321784006667845622477657312754389262271342073231045816593267889580&'}, 'transcript': b'axvcE9uTNcMdJg==&Ah1gUhyiZ+mkZlD2+TRbQ0XcHeINJZ2q0oqcPw5XVOnl&AwHsAWZ/YjBDeDFq/wDqPzynI71Y5GltcnG8b5MCXy7Q&60241583463011578596754492933374845129114558045040091300664579946831999469866&88506663360127818033053368572772810055211223973528053370294345329481892265545&AiYB2KAbbGo9KETOffkq5Kj46RPEbZeOyGF8VOj+E2JO&Ani91Fd/SNwYkdXfOvABm6HutAcjAXuGK8Zi6GRjzgH+&457758319185783083555530462566442675169657717388595593977308165104806501998&'}}"""
	# start_time = time.time()
	authSpenders(owner_address,"0x85805Ae2052EEa616db6c1A08e19d326Dac756B6")
	callUploadDate("0x85805Ae2052EEa616db6c1A08e19d326Dac756B6",proof)
	# end_time = time.time()
	# run_time = end_time - start_time
	# print(f"程序运行时间：{run_time} 秒")
	# start_time = time.time()
	# authRecievers(owner_address,"0xdDb627D116FCde7F60261b9cd67C2a153247C3A9")
	# callDownloaddata("0xdDb627D116FCde7F60261b9cd67C2a153247C3A9")
	# end_time = time.time()
	# run_time = end_time - start_time
	# print(f"程序运行时间：{run_time} 秒")




