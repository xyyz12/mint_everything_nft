# mint_everything_nft
mint nft通用版教程，参考大佬

参考：https://twitter.com/gm365/status/1733006815296954379

https://explorer.zksync.io/tx/0xe7e8e824670389986c09bd962c0a82327650099177a30032ffff6076ef94fb33

![bff1e555ab36305845606f1594a6f13](https://github.com/xyyz12/mint_everything_nft/assets/91812763/aef49af9-1670-4027-9aa8-738c86471b96)

![a7a75b0c9a635e709e7e950be1b6dc7](https://github.com/xyyz12/mint_everything_nft/assets/91812763/3a70e050-ded3-4e30-8673-96ebbaac2d1e)

从这笔 mint 交易可以看到，参数只有三个：

tokenId  +  amount  +  signature

绝大部分情况，这些信息都是从服务器后端的API接口请求而来的。极少数情况，签名是直接在本地的浏览器环境生成的。但这种安全系数不太高，所以用的较少刚好，我们的情况属于多数情况

👉 打开浏览器的 Inspect 开发者工具，切换到 Network 网络请求，选中 Fetch/XHR 标签，专注于这些向服务器API发送的异步请求

打开了开发者工具后，再次模拟一遍 Mint NFT 的动作，尤其注意那些在小狐狸窗口  “弹出前”  的几个请求，这些一般是最重要的参数传递请求

比如，我们很容易就发现了这条叫 claim_sign_award 的请求，其传送回来的 data 内容里，包含了所有我们需要的信息：

tokenId  +  amount  +  signature  +  address

![image](https://github.com/xyyz12/mint_everything_nft/assets/91812763/57398909-cbb8-4cc6-afe0-2eaacfbb6570)

🎯 目标出现，接下来，我们的方向就转向了如何模拟这条请求，获取需要的参数





