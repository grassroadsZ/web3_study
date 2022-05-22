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
    print(f"{from_address} 的 地址余额 为 {float(from_address_balance / 1e18)} ETH,转账 {l1_amount / 1e18} ETH")

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
        print(f"{from_address} 的 地址余额 为 {float(from_address_balance / 1e18)} ETH")

        return {'status': 'succeed', 'txn_hash': web3_instance.toHex(txn), 'task': 'Bridge ETH'}

    except Exception as e:
        return {'status': 'failed', 'error': e, 'task': 'Bridge ETH'}


def zks_bridge(from_address, from_address_private_key, l1_amount):
    ZKS_Contract = "0x578bade599406a8fe3d24fd7f7211c0911f5b29e"
    Contract_ABI = '[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint32","name":"blockNumber","type":"uint32"}],"name":"BlockCommit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint32","name":"blockNumber","type":"uint32"}],"name":"BlockExecution","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint32","name":"totalBlocksVerified","type":"uint32"},{"indexed":false,"internalType":"uint32","name":"totalBlocksCommitted","type":"uint32"}],"name":"BlocksRevert","type":"event"},{"anonymous":false,"inputs":[{"components":[{"internalType":"address","name":"facet","type":"address"},{"internalType":"enum Diamond.Action","name":"action","type":"uint8"},{"internalType":"bool","name":"isFreezable","type":"bool"},{"internalType":"bytes4[]","name":"selectors","type":"bytes4[]"}],"indexed":false,"internalType":"struct Diamond.FacetCut[]","name":"_facetCuts","type":"tuple[]"},{"indexed":false,"internalType":"address","name":"_initAddress","type":"address"}],"name":"DiamondCutProposal","type":"event"},{"anonymous":false,"inputs":[],"name":"DiamondCutProposalCancelation","type":"event"},{"anonymous":false,"inputs":[{"components":[{"components":[{"internalType":"address","name":"facet","type":"address"},{"internalType":"enum Diamond.Action","name":"action","type":"uint8"},{"internalType":"bool","name":"isFreezable","type":"bool"},{"internalType":"bytes4[]","name":"selectors","type":"bytes4[]"}],"internalType":"struct Diamond.FacetCut[]","name":"facetCuts","type":"tuple[]"},{"internalType":"address","name":"initAddress","type":"address"},{"internalType":"bytes","name":"initCalldata","type":"bytes"}],"indexed":false,"internalType":"struct Diamond.DiamondCutData","name":"_diamondCut","type":"tuple"}],"name":"DiamondCutProposalExecution","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"_address","type":"address"}],"name":"EmergencyDiamondCutApproved","type":"event"},{"anonymous":false,"inputs":[],"name":"EmergencyFreeze","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint32","name":"expirationBlock","type":"uint32"},{"indexed":false,"internalType":"uint64[]","name":"operationIDs","type":"uint64[]"},{"indexed":false,"internalType":"enum Operations.OpTree","name":"opTree","type":"uint8"}],"name":"MovePriorityOperationsFromBufferToHeap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"newGovernor","type":"address"}],"name":"NewGovernor","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"enum Operations.OpTree","name":"opTree","type":"uint8"},{"indexed":false,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint96","name":"bidAmount","type":"uint96"},{"indexed":false,"internalType":"uint256","name":"complexity","type":"uint256"}],"name":"NewPriorityModeAuctionBid","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"enum PriorityModeLib.Epoch","name":"subEpoch","type":"uint8"},{"indexed":false,"internalType":"uint128","name":"subEpochEndTimestamp","type":"uint128"}],"name":"NewPriorityModeSubEpoch","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint64","name":"serialId","type":"uint64"},{"indexed":false,"internalType":"bytes","name":"opMetadata","type":"bytes"}],"name":"NewPriorityRequest","type":"event"},{"anonymous":false,"inputs":[],"name":"PriorityModeActivated","type":"event"},{"anonymous":false,"inputs":[],"name":"Unfreeze","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"validatorAddress","type":"address"},{"indexed":false,"internalType":"bool","name":"isActive","type":"bool"}],"name":"ValidatorStatusUpdate","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"zkSyncTokenAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"WithdrawPendingBalance","type":"event"},{"inputs":[{"internalType":"uint32","name":"_ethExpirationBlock","type":"uint32"}],"name":"activatePriorityMode","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_token","type":"address"},{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint8","name":"_decimals","type":"uint8"},{"internalType":"enum Operations.QueueType","name":"_queueType","type":"uint8"},{"internalType":"enum Operations.OpTree","name":"_opTree","type":"uint8"}],"name":"addCustomToken","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"_token","type":"address"},{"internalType":"enum Operations.QueueType","name":"_queueType","type":"uint8"},{"internalType":"enum Operations.OpTree","name":"_opTree","type":"uint8"}],"name":"addToken","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_gasPrice","type":"uint256"},{"internalType":"enum Operations.QueueType","name":"_queueType","type":"uint8"},{"internalType":"enum Operations.OpTree","name":"_opTree","type":"uint8"}],"name":"addTokenBaseCost","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_diamondCutHash","type":"bytes32"}],"name":"approveEmergencyDiamondCutAsSecurityCouncilMember","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"cancelDiamondCutProposal","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_newGovernor","type":"address"}],"name":"changeGovernor","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint32","name":"blockNumber","type":"uint32"},{"internalType":"uint16","name":"numberOfLayer1Txs","type":"uint16"},{"internalType":"uint16","name":"numberOfLayer2Txs","type":"uint16"},{"internalType":"uint224","name":"priorityOperationsComplexity","type":"uint224"},{"internalType":"bytes32","name":"processableOnchainOperationsHash","type":"bytes32"},{"internalType":"bytes32","name":"priorityOperationsHash","type":"bytes32"},{"internalType":"uint256","name":"timestamp","type":"uint256"},{"internalType":"bytes32","name":"stateRoot","type":"bytes32"},{"internalType":"bytes32","name":"zkPorterRoot","type":"bytes32"},{"internalType":"bytes32","name":"commitment","type":"bytes32"}],"internalType":"struct IExecutor.StoredBlockInfo","name":"_lastCommittedBlockData","type":"tuple"},{"components":[{"internalType":"bytes32","name":"newStateRoot","type":"bytes32"},{"internalType":"bytes32","name":"zkPorterRoot","type":"bytes32"},{"internalType":"uint32","name":"blockNumber","type":"uint32"},{"internalType":"address","name":"feeAccount","type":"address"},{"internalType":"uint256","name":"timestamp","type":"uint256"},{"internalType":"uint224","name":"priorityOperationsComplexity","type":"uint224"},{"internalType":"uint16","name":"numberOfLayer1Txs","type":"uint16"},{"internalType":"uint16","name":"numberOfLayer2Txs","type":"uint16"},{"internalType":"bytes32","name":"processableOnchainOperationsHash","type":"bytes32"},{"internalType":"bytes32","name":"priorityOperationsHash","type":"bytes32"},{"internalType":"bytes","name":"deployedContracts","type":"bytes"},{"internalType":"bytes","name":"storageUpdateLogs","type":"bytes"},{"components":[{"internalType":"uint32","name":"round","type":"uint32"},{"components":[{"internalType":"bytes","name":"pubkey","type":"bytes"},{"internalType":"bytes","name":"signature","type":"bytes"}],"internalType":"struct IExecutor.PublicWithSignature[]","name":"sigs","type":"tuple[]"},{"internalType":"uint32","name":"stake","type":"uint32"}],"internalType":"struct IExecutor.QuorumSigs","name":"zkPorterData","type":"tuple"}],"internalType":"struct IExecutor.CommitBlockInfo[]","name":"_newBlocksData","type":"tuple[]"}],"name":"commitBlocks","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_gasPrice","type":"uint256"},{"internalType":"uint256","name":"_ergsLimit","type":"uint256"},{"internalType":"uint32","name":"_bytecodeLength","type":"uint32"},{"internalType":"uint32","name":"_calldataLength","type":"uint32"},{"internalType":"enum Operations.QueueType","name":"_queueType","type":"uint8"},{"internalType":"enum Operations.OpTree","name":"_opTree","type":"uint8"}],"name":"deployContractBaseCost","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_gasPrice","type":"uint256"},{"internalType":"enum Operations.QueueType","name":"_queueType","type":"uint8"},{"internalType":"enum Operations.OpTree","name":"_opTree","type":"uint8"}],"name":"depositBaseCost","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"_token","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"address","name":"_zkSyncAddress","type":"address"},{"internalType":"enum Operations.QueueType","name":"_queueType","type":"uint8"},{"internalType":"enum Operations.OpTree","name":"_opTree","type":"uint8"}],"name":"depositERC20","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"address","name":"_zkSyncAddress","type":"address"},{"internalType":"enum Operations.QueueType","name":"_queueType","type":"uint8"},{"internalType":"enum Operations.OpTree","name":"_opTree","type":"uint8"}],"name":"depositETH","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"emergencyFreezeDiamond","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_gasPrice","type":"uint256"},{"internalType":"uint256","name":"_ergsLimit","type":"uint256"},{"internalType":"uint32","name":"_calldataLength","type":"uint32"},{"internalType":"enum Operations.QueueType","name":"_queueType","type":"uint8"},{"internalType":"enum Operations.OpTree","name":"_opTree","type":"uint8"}],"name":"executeBaseCost","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"components":[{"internalType":"uint32","name":"blockNumber","type":"uint32"},{"internalType":"uint16","name":"numberOfLayer1Txs","type":"uint16"},{"internalType":"uint16","name":"numberOfLayer2Txs","type":"uint16"},{"internalType":"uint224","name":"priorityOperationsComplexity","type":"uint224"},{"internalType":"bytes32","name":"processableOnchainOperationsHash","type":"bytes32"},{"internalType":"bytes32","name":"priorityOperationsHash","type":"bytes32"},{"internalType":"uint256","name":"timestamp","type":"uint256"},{"internalType":"bytes32","name":"stateRoot","type":"bytes32"},{"internalType":"bytes32","name":"zkPorterRoot","type":"bytes32"},{"internalType":"bytes32","name":"commitment","type":"bytes32"}],"internalType":"struct IExecutor.StoredBlockInfo","name":"storedBlock","type":"tuple"},{"internalType":"bytes","name":"processableOnchainOperations","type":"bytes"}],"internalType":"struct IExecutor.ExecuteBlockInfo[]","name":"_blocksData","type":"tuple[]"}],"name":"executeBlocks","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"components":[{"internalType":"address","name":"facet","type":"address"},{"internalType":"enum Diamond.Action","name":"action","type":"uint8"},{"internalType":"bool","name":"isFreezable","type":"bool"},{"internalType":"bytes4[]","name":"selectors","type":"bytes4[]"}],"internalType":"struct Diamond.FacetCut[]","name":"facetCuts","type":"tuple[]"},{"internalType":"address","name":"initAddress","type":"address"},{"internalType":"bytes","name":"initCalldata","type":"bytes"}],"internalType":"struct Diamond.DiamondCutData","name":"_diamondCut","type":"tuple"}],"name":"executeDiamondCutProposal","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getGovernor","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_address","type":"address"},{"internalType":"address","name":"_token","type":"address"}],"name":"getPendingBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTotalBlocksCommitted","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTotalBlocksExecuted","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTotalBlocksVerified","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTotalPriorityRequests","outputs":[{"internalType":"uint64","name":"","type":"uint64"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getVerifier","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_address","type":"address"}],"name":"isValidator","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_nOpsToMove","type":"uint256"},{"internalType":"enum Operations.OpTree","name":"_opTree","type":"uint8"}],"name":"movePriorityOpsFromBufferToMainQueue","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint112","name":"_complexityRoot","type":"uint112"},{"internalType":"enum Operations.OpTree","name":"_opTree","type":"uint8"}],"name":"placeBidForBlocksProcessingAuction","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"facet","type":"address"},{"internalType":"enum Diamond.Action","name":"action","type":"uint8"},{"internalType":"bool","name":"isFreezable","type":"bool"},{"internalType":"bytes4[]","name":"selectors","type":"bytes4[]"}],"internalType":"struct Diamond.FacetCut[]","name":"_facetCuts","type":"tuple[]"},{"internalType":"address","name":"_initAddress","type":"address"}],"name":"proposeDiamondCut","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint32","name":"blockNumber","type":"uint32"},{"internalType":"uint16","name":"numberOfLayer1Txs","type":"uint16"},{"internalType":"uint16","name":"numberOfLayer2Txs","type":"uint16"},{"internalType":"uint224","name":"priorityOperationsComplexity","type":"uint224"},{"internalType":"bytes32","name":"processableOnchainOperationsHash","type":"bytes32"},{"internalType":"bytes32","name":"priorityOperationsHash","type":"bytes32"},{"internalType":"uint256","name":"timestamp","type":"uint256"},{"internalType":"bytes32","name":"stateRoot","type":"bytes32"},{"internalType":"bytes32","name":"zkPorterRoot","type":"bytes32"},{"internalType":"bytes32","name":"commitment","type":"bytes32"}],"internalType":"struct IExecutor.StoredBlockInfo[]","name":"_committedBlocks","type":"tuple[]"},{"components":[{"internalType":"uint256[]","name":"recursiveInput","type":"uint256[]"},{"internalType":"uint256[]","name":"proof","type":"uint256[]"},{"internalType":"uint256[]","name":"commitments","type":"uint256[]"},{"internalType":"uint8[]","name":"vkIndexes","type":"uint8[]"},{"internalType":"uint256[16]","name":"subproofsLimbs","type":"uint256[16]"}],"internalType":"struct IExecutor.ProofInput","name":"_proof","type":"tuple"}],"name":"proveBlocks","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes","name":"_bytecode","type":"bytes"},{"internalType":"bytes","name":"_calldata","type":"bytes"},{"internalType":"uint256","name":"_ergsLimit","type":"uint256"},{"internalType":"enum Operations.QueueType","name":"_queueType","type":"uint8"},{"internalType":"enum Operations.OpTree","name":"_opTree","type":"uint8"}],"name":"requestDeployContract","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_contractAddressL2","type":"address"},{"internalType":"bytes","name":"_calldata","type":"bytes"},{"internalType":"uint256","name":"_ergsLimit","type":"uint256"},{"internalType":"enum Operations.QueueType","name":"_queueType","type":"uint8"},{"internalType":"enum Operations.OpTree","name":"_opTree","type":"uint8"}],"name":"requestExecute","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_token","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"address","name":"_to","type":"address"},{"internalType":"enum Operations.QueueType","name":"_queueType","type":"uint8"},{"internalType":"enum Operations.OpTree","name":"_opTree","type":"uint8"}],"name":"requestWithdraw","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint32","name":"_blocksToRevert","type":"uint32"}],"name":"revertBlocks","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_validator","type":"address"},{"internalType":"bool","name":"_active","type":"bool"}],"name":"setValidator","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"unfreezeDiamond","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"updatePriorityModeSubEpoch","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_gasPrice","type":"uint256"},{"internalType":"enum Operations.QueueType","name":"_queueType","type":"uint8"},{"internalType":"enum Operations.OpTree","name":"_opTree","type":"uint8"}],"name":"withdrawBaseCost","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address payable","name":"_owner","type":"address"},{"internalType":"address","name":"_token","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdrawPendingBalance","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
    web3_instance = connect_web3_instance("goerli")
    params = {

        'gas': 250000,
        'nonce': web3_instance.eth.getTransactionCount(web3_instance.toChecksumAddress(from_address)),
        'from': web3_instance.toChecksumAddress(from_address),
        'value': web3_instance.toWei(l1_amount, "ether"),
        # 'gasPrice': w3.toWei('5', 'gwei'),
        'maxFeePerGas': web3_instance.toWei(5, 'gwei'),
        'maxPriorityFeePerGas': web3_instance.toWei(5, 'gwei'),
        'chainId': 5,
        "type": "0x2",
    }
    ZksContractInstance = web3_instance.eth.contract(Web3.toChecksumAddress(ZKS_Contract), abi=Contract_ABI)
    function_instance = ZksContractInstance.functions.depositETH(_amount=web3_instance.toWei(l1_amount, "ether"),
                                                                 _zkSyncAddress=web3_instance.toChecksumAddress(
                                                                     from_address), _queueType=0, _opTree=0)

    try:
        # 构建tx
        tx = function_instance.buildTransaction(params)
        # 签名
        sign_tx = web3_instance.eth.account.signTransaction(tx, private_key=from_address_private_key)
        # 发送交易
        txn = web3_instance.eth.sendRawTransaction(sign_tx.rawTransaction)
        from_address_balance = web3_instance.eth.get_balance(web3_instance.toChecksumAddress(from_address))
        print(f"{from_address} 的 地址余额 为 {float(from_address_balance / 1e18)} ETH")

        return {'status': 'succeed', 'txn_hash': web3_instance.toHex(txn), 'task': 'Bridge ETH'}

    except Exception as e:
        return {'status': 'failed', 'error': e, 'task': 'Bridge ETH'}


if __name__ == '__main__':
    # lesson_02()
    # lesson_03()
    # print(bridge_arbitrum(from_address="0xa997B77dE801f787e14ebCe46eb7c599F6366Fc5",
    #                       from_address_private_key=os.getenv('TEST_ACCOUNT_SECRET'), l1_amount=0.2))

    print(zks_bridge(from_address="0xa997b77de801f787e14ebce46eb7c599f6366fc5",
                     from_address_private_key=os.getenv('TEST_ACCOUNT_SECRET'), l1_amount=0.001))
