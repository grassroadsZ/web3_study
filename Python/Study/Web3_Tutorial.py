"""

来源于: https://github.com/gm365/Web3_Tutorial
"""

import os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()


def connect_web3_instance(network="mainnet"):
    # 使用dotenv 进行配置的管理 此处只需要使用 Infura 的project_id 即可
    INFURA_PROJECT_ID = os.getenv('INFURA_PROJECT_ID')
    INFURA_MAIN_NETWORK = f'https://{network}.infura.io/v3/{INFURA_PROJECT_ID}'

    web3_instance = Web3(Web3.HTTPProvider(endpoint_uri=INFURA_MAIN_NETWORK))
    print(web3_instance.isConnected())
    return web3_instance


def lesson_01():
    """
     前期准备工作
    """
    print("pip install web3")
    print("register https://infura.io/ , and get a api key")


def lesson_02():
    """
    通过 Infura 接入以太坊主网并查询钱包余额信息
    """
    web3_instance = connect_web3_instance()
    # 判断是否连接
    print(web3_instance.isConnected())

    # 当前区块高度
    print(web3_instance.eth.block_number)

    # V神 3号钱包地址
    vb = '0x220866b1a2219f40e72f5c628b65d54268ca3a9d'

    # 地址格式转换
    address = Web3.toChecksumAddress(vb)

    # 查询地址 ETH余额 返回的wei是最小的以太单位 使用fromWei 将任何WEI值转换为以太值。
    balance = web3_instance.eth.get_balance(address)

    balance = float(web3_instance.fromWei(balance, 'ether'))
    print(f'V神地址余额: {balance} ETH')


def lesson_03():
    """
    接入 Rinkeby 测试网并完成一笔转账交易
    地址 0x365a800a3c6a6B73B29E052fd4F7e68BFD45A086
    私钥：e2facfbd1f0736318382d87b81029b05b7650ba17467c844cea5998a40e5bbc2
    转账hash ：0xb8dd826ca1dee9744a4e06fe7e543930c975e973fefcbeb12444547a111bdd4f
    """

    def transfer_eth(w3, from_address, private_key, target_address, amount, gas_price=5, gas_limit=21000, chainId=4):
        # Web3.toChecksumAddress 将给定的大写或小写以太坊地址转换为校验后的地址
        from_address = Web3.toChecksumAddress(from_address)
        target_address = Web3.toChecksumAddress(target_address)
        nonce = w3.eth.getTransactionCount(from_address)  # 获取 nonce(地址发出的交易总数量) 值
        params = {
            'from': from_address,
            'nonce': nonce,
            'to': target_address,
            'value': w3.toWei(amount, 'ether'),
            'gas': gas_limit,
            # 'gasPrice': w3.toWei(gas_price, 'gwei'),
            'maxFeePerGas': w3.toWei(gas_price, 'gwei'),
            'maxPriorityFeePerGas': w3.toWei(gas_price, 'gwei'),
            'chainId': chainId,

        }
        try:
            signed_tx = w3.eth.account.signTransaction(params, private_key=private_key)
            txn = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            return {'status': 'succeed', 'txn_hash': w3.toHex(txn), 'task': 'Transfer ETH'}
        except Exception as e:
            return {'status': 'failed', 'error': e, 'task': 'Transfer ETH'}

    from_address = "0x365a800a3c6a6B73B29E052fd4F7e68BFD45A086"

    # 测试转入地址
    to_address = "0x8888a4E88f66f9C9FCE8c25F193617F3a3aB0760"
    rinkeby_test_private_key = "e2facfbd1f0736318382d87b81029b05b7650ba17467c844cea5998a40e5bbc2"

    web3_instance = connect_web3_instance("rinkeby")

    balance_wei = web3_instance.eth.get_balance(Web3.toChecksumAddress(from_address))
    balance = float(Web3.toWei(balance_wei, "ether"))
    print(f'当前地址余额: {balance} ETH')

    # 转账 ETH 金额
    amount = 0.001

    # Rinkeby Chain ID
    chainId = 4
    result = transfer_eth(web3_instance, from_address, rinkeby_test_private_key, to_address, amount, chainId=chainId)
    print(result)

    balance_wei = web3_instance.eth.get_balance(Web3.toChecksumAddress(from_address))
    balance = float(Web3.toWei(balance_wei, "ether"))
    print(f'当前地址余额: {balance} ETH')




if __name__ == '__main__':
    # lesson_02()
    lesson_03()
