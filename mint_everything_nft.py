import time
import requests
from web3 import Web3
from eth_account.messages import encode_defunct

class MyClass:
    def get_bearer_token(self, from_address, private_key):
        #获取当前时间戳
        timestamp = int(time.time())
        
        #签名消息
        message = from_address + str(timestamp)
        encoded_message = encode_defunct(text=message)
        signed_message = Web3().eth.account.sign_message(encoded_message, private_key=private_key)
        
        signature = signed_message.signature.hex()
        
        #转被请求http头部
        headers = {
            "accept": "application/json, text/plain, */*",
            "origin": "https://game.theanimalage.com",
            "referer": "https://game.theanimalage.com/",
            "user-agent": "Mozilla/5.0"
        }
        
        #准备查询参数
        params = {
            "address": from_address,
            "signature": signature,
            "timestamp": str(timestamp)
        }
        
        #发送请求以获取 bearer token
        response = requests.get("https://api.theanimalage.com/api/login", 
            params=params, 
            headers=headers, 
            timeout=8
        )
        response_data = response.json()
        
        
        #检查响应是否成功
        if response_data.get("code") == 1:
            #返回 bearer token
            return response_data.get("data").get("token")
        else:
            #返回错误信息
            raise ValueError("Failed to retrieve bearer token: " + response_data.get("msg"))

    def get_headers(self, bearer_token):
        #准备请求http头部
        headers = {
            "accept": "application/json, text/plain, */*",
            "authorization": f"Bearer {bearer_token}",
            "origin": "https://game.theanimalage.com",
            "referer": "https://game.theanimalage.com/",
            "user-agent": "Mozilla/5.0"
        }
        return headers

    def check_in(self, from_address, headers):
        try:
            response = requests.post("https://api.theanimalage.com/api/do_sign", headers=headers, json={"address": from_address}, timeout=8).json()
            code = response.get("code")
            msg = response.get("msg")
            if code == 0 and "You have signed" in msg:
                print(f"√ 今日已签到 ->: {msg}")
            elif code in [0, 1]:
                print(f" 签到成功 ->: {msg}")
            else:
                print(f"X签到失败 ->: {msg}")
        except Exception as e:
            print(f"X 签到失败: {e}")

    def get_claimable_token_ids(self, from_address, headers):
        json_data = {"address": from_address}
        response = requests.post("https://api.theanimalage.com/api/task/1", headers=headers, json=json_data, timeout=8)
        try:
            result = response.json()
            task_award = result["data"]["task_award"]
            token_ids = [item["tokenid"] for item in task_award]
            return token_ids
        except Exception as e:
            print(f"X获取可领取的 NFT 失败: {e}")
            return []

    def get_claim_token_signature(self, from_address, token_id, headers):
        json_data = {"address": from_address, "token_id": token_id}
        try:
            response = requests.post("https://api.theanimalage.com/api/claim_sign_award", headers=headers, json=json_data, timeout=8).json()
            return response["data"]["signature"]
        except Exception as e:
            print(f"X 获取 NFT {token_id} 的签名失败: {e}")
            return None

    def mint(self, web3, token_id, amount, signature):
        contract_address = "0xe0e9e2f208eb5c953345526bcb515120128298cf"
        to_address = web3.toChecksumAddress(contract_address)
        abi = [
            # check in
            # mint NFT
            {
                "constant": False,
                "inputs": [
                    {"name": "tokenId", "type": "uint256"},
                    {"name": "amount", "type": "uint256"},
                    {"name": "signature", "type": "bytes"}
                ],
                "name": "mint",
                "outputs": [],
                "payable": False,
                "stateMutability": "nonpayable",
                "type": "function"
            }
        ]
        contract = web3.eth.contract(address=to_address, abi=abi)
        return contract.functions.mint(token_id, amount, signature)

    def mint_nft_call(self, from_address, private_key, token_id, signature, amount):
        
        print(f"Mint NFT: {token_id}")
        func = self.mint(self.web3, token_id, amount, signature)
        value = 0
        return self.helper.call_contract_function(from_address, private_key, func, value)

    def task(self, from_address, private_key):
        print(" 执行 Animal Age 任务中...")
        from_address = self.web3.to_Checksum_Address(from_address)
       
        print("获取 bearer token 相关信息")
        bearer_token = self.get_bearer_token(from_address, private_key)
        
        time.sleep(random.randint(LONG_WAIT_TIME_MIN, LONG_WAIT_TIME_MAX))
        
        #准备 HTTP 请求头部
        headers = self.get_headers(bearer_token)
        
        time.sleep(random.randint(LONG_WAIT_TIME_MIN, LONG_WAIT_TIME_MAX))
        
        #签到
        print(" Step 1: check in")
        self.check_in(from_address, headers)
        
        time.sleep(random.randint(LONG_WAIT_TIME_MIN, LONG_WAIT_TIME_MAX))
        time.sleep(random.randint(LONG_WAIT_TIME_MIN, LONG_WAIT_TIME_MAX))
        
        print(" Step 2: get claimable token ids")
        token_ids = self.get_claimable_token_ids(from_address, headers)
       
        if not len(token_ids):
            print("没有可领取的 NFT")
        else:
            print(f"NFT 当前可领取: {len(token_ids)} 枚 -> {token_ids}")
            
            claim_count = random.randint(1, len(token_ids))
            
            # 从 token_ids 中随机选择 claim_count 个不同的 token_id
            claim_token_ids = random.sample(token_ids, claim_count)
            
            print(f"随机领取: {claim_count} 枚 -> {claim_token_ids}")
            
            print(" Step 3: claim token")
            
            for token_id in claim_token_ids:
                #获取签名
                print(f" Step 4: get claim token signature")
                signature = self.get_claim_token_signature(from_address, token_id, headers)
                
                time.sleep(random.randint(LONG_WAIT_TIME_MIN, LONG_WAIT_TIME_MAX))
                
                print(f" Step 5: mint NFT: {token_id}")
                success = self.mint_nft_call(from_address, private_key, token_id, signature)
                
                if success:
                    print(f"√ NFT {token_id} mint 完成")
                else:
                    print(f"! NFT {token_id} mint 失败")
                    
                time.sleep(random.randint(LONG_WAIT_TIME_MIN, LONG_WAIT_TIME_MAX))
                time.sleep(random.randint(LONG_WAIT_TIME_MIN, LONG_WAIT_TIME_MAX))
                time.sleep(random.randint(LONG_WAIT_TIME_MIN, LONG_WAIT_TIME_MAX))
                
        print("Animal Age 任务执行完毕")