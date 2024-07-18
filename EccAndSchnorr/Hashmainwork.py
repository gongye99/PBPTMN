import hashlib

def hash_data(data):
    # 创建一个sha256哈希对象
    hash_object = hashlib.sha256()
    # 提供要哈希的数据，必须是字节串
    hash_object.update(data.encode())
    # 获取哈希值的十六进制表示
    hash_hex = hash_object.hexdigest()
    return hash_hex

# 使用示例
if __name__ == '__main__':
    data = "Hello, Hashing!"
    hashed_data = hash_data(data)
    print(f"原始数据: {data}")
    print(f"哈希值: {hashed_data}")
    hashed_data = hash_data(data)
    print(f"哈希值: {hashed_data}")