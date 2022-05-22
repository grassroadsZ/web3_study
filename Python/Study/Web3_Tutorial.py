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


def bridge_arbitrum(from_address, from_address_private_key, l1_amount):
    """
    Arbitrum 测试网跨链桥
    """
    ArbitrumProxyContract = "0x578BAde599406A8fE3d24Fd7f7211c0911F5B29e"
    ArbitrumProxyContractAbi = '[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"messageNum","type":"uint256"},{"indexed":false,"internalType":"bytes","name":"data","type":"bytes"}],"name":"InboxMessageDelivered","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"messageNum","type":"uint256"}],"name":"InboxMessageDeliveredFromOrigin","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"enabled","type":"bool"}],"name":"PauseToggled","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"enabled","type":"bool"}],"name":"RewriteToggled","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"newSource","type":"address"}],"name":"WhitelistSourceUpdated","type":"event"},{"inputs":[],"name":"bridge","outputs":[{"internalType":"contract IBridge","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"destAddr","type":"address"},{"internalType":"uint256","name":"l2CallValue","type":"uint256"},{"internalType":"uint256","name":"maxSubmissionCost","type":"uint256"},{"internalType":"address","name":"excessFeeRefundAddress","type":"address"},{"internalType":"address","name":"callValueRefundAddress","type":"address"},{"internalType":"uint256","name":"maxGas","type":"uint256"},{"internalType":"uint256","name":"gasPriceBid","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"createRetryableTicket","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"destAddr","type":"address"},{"internalType":"uint256","name":"l2CallValue","type":"uint256"},{"internalType":"uint256","name":"maxSubmissionCost","type":"uint256"},{"internalType":"address","name":"excessFeeRefundAddress","type":"address"},{"internalType":"address","name":"callValueRefundAddress","type":"address"},{"internalType":"uint256","name":"maxGas","type":"uint256"},{"internalType":"uint256","name":"gasPriceBid","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"createRetryableTicketNoRefundAliasRewrite","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"maxSubmissionCost","type":"uint256"}],"name":"depositEth","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"contract IBridge","name":"_bridge","type":"address"},{"internalType":"address","name":"_whitelist","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"isCreateRetryablePaused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"isMaster","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pauseCreateRetryables","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"maxGas","type":"uint256"},{"internalType":"uint256","name":"gasPriceBid","type":"uint256"},{"internalType":"address","name":"destAddr","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"sendContractTransaction","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"maxGas","type":"uint256"},{"internalType":"uint256","name":"gasPriceBid","type":"uint256"},{"internalType":"address","name":"destAddr","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"sendL1FundedContractTransaction","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"maxGas","type":"uint256"},{"internalType":"uint256","name":"gasPriceBid","type":"uint256"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"address","name":"destAddr","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"sendL1FundedUnsignedTransaction","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes","name":"messageData","type":"bytes"}],"name":"sendL2Message","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes","name":"messageData","type":"bytes"}],"name":"sendL2MessageFromOrigin","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"maxGas","type":"uint256"},{"internalType":"uint256","name":"gasPriceBid","type":"uint256"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"address","name":"destAddr","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"sendUnsignedTransaction","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"shouldRewriteSender","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startRewriteAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"stopRewriteAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"unpauseCreateRetryables","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"destAddr","type":"address"},{"internalType":"uint256","name":"l2CallValue","type":"uint256"},{"internalType":"uint256","name":"maxSubmissionCost","type":"uint256"},{"internalType":"address","name":"excessFeeRefundAddress","type":"address"},{"internalType":"address","name":"callValueRefundAddress","type":"address"},{"internalType":"uint256","name":"maxGas","type":"uint256"},{"internalType":"uint256","name":"gasPriceBid","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"unsafeCreateRetryableTicket","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"newSource","type":"address"}],"name":"updateWhitelistSource","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"whitelist","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'
    web3_instance = connect_web3_instance("rinkeby")

    # 通过合约地址 以及abi 实例化的 对象才可以使用abi中的方法进行调用
    ArbitrumProxyContractInstance = web3_instance.eth.contract(address=Web3.toChecksumAddress(ArbitrumProxyContract),
                                                               abi=ArbitrumProxyContractAbi)

    l1_amount = web3_instance.toWei(l1_amount, "ether")
    from_address_balance = web3_instance.eth.get_balance(web3_instance.toChecksumAddress(from_address))
    print(f"{from_address} 的 地址余额 为 {float(from_address_balance/1e18)} ETH,转账 {l1_amount/1e18} ETH")

    function_instance = ArbitrumProxyContractInstance.functions.depositEth(maxSubmissionCost=l1_amount)

    params = {

        'gas': 250000,
        'nonce': web3_instance.eth.getTransactionCount(web3_instance.toChecksumAddress(from_address)),
        'from': web3_instance.toChecksumAddress(from_address),
        'value': l1_amount,
        # 'gasPrice': w3.toWei('5', 'gwei'),
        'maxFeePerGas': web3_instance.toWei(5, 'gwei'),
        'maxPriorityFeePerGas': web3_instance.toWei(5, 'gwei'),
        'chainId': 4,

    }
    try:
        # 构建tx
        tx = function_instance.buildTransaction(params)
        # 签名
        sign_tx = web3_instance.eth.account.signTransaction(tx, private_key=from_address_private_key)
        # 发送交易
        txn = web3_instance.eth.sendRawTransaction(sign_tx.rawTransaction)
        from_address_balance = web3_instance.eth.get_balance(web3_instance.toChecksumAddress(from_address))
        print(f"{from_address} 的 地址余额 为 {float(from_address_balance/1e18)} ETH")

        return {'status': 'succeed', 'txn_hash': web3_instance.toHex(txn), 'task': 'Bridge ETH'}

    except Exception as e:
        return {'status': 'failed', 'error': e, 'task': 'Bridge ETH'}


if __name__ == '__main__':
    # lesson_02()
    # lesson_03()
    print(bridge_arbitrum(from_address="0xa997B77dE801f787e14ebCe46eb7c599F6366Fc5",
                          from_address_private_key=os.getenv('TEST_ACCOUNT_SECRET'), l1_amount=0.2))
