from web3 import Web3

# Ganache 默认URL
ganache_url = "http://localhost:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# 检查是否连接成功
print(web3.is_connected())

transaction_hash = '0x945b2132e2ea7aaf9fe219171d4d8ac679c1e45427ec58163fb9fb5fc8bb5323'

# 获取交易
transaction = web3.eth.get_transaction(transaction_hash)
print(transaction)

# 计算交易大小
transaction_input = transaction['input']

# 计算十六进制字符串表示的大小（字节为单位）
transaction_size_approx = len(transaction_input) // 2

print("Approximate transaction size in bytes:", transaction_size_approx)

# 获取交易时间
block = web3.eth.get_block(transaction.blockNumber)
transaction_time = block.timestamp
print("Transaction time:", transaction_time)

# 获取交易收据来计算Gas成本
receipt = web3.eth.get_transaction_receipt(transaction_hash)
gas_cost = receipt.gasUsed
print("Gas cost:", gas_cost)

# 获取交易的Gas价格
gas_price = transaction.gasPrice
print(gas_price)
# 计算交易的ETH成本，转换为ETH单位
eth_cost = web3.from_wei(gas_cost * gas_price, 'ether')
print("Transaction ETH cost:", eth_cost)
