# DMXAPI 用户信息接口

## 接口地址
`GET https://www.dmxapi.cn/api/user/self`

## 认证方式
需要在请求头中携带系统访问令牌

获取路径： 登录DMXAPI → 工作台 → 个人设置 → 更多选项 → 系统令牌

## 请求示例
```python
import requests

# 1. 配置请求参数
url = "https://www.dmxapi.cn/api/user/self"
system_token = "your_system_token"  # 替换为你的系统令牌

headers = {
    "Accept": "application/json",
    "Authorization": f"{system_token}",  # 认证头	
    "Rix-Api-User": "你的用户ID",  # 刚改为你的用户ID，在 个人设置 中获得

}

# 2. 发送GET请求
response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()  # 检查请求是否成功

# 3. 处理响应数据
data = response.json()
quota = data["data"]["quota"]  # 获取账户额度
balance = quota / 500000  # 转换为人民币金额

# 4. 输出结果
print(f"账户额度: {quota:,}")
print(f"人民币余额: ￥{balance:.6f}")
```

## 响应说明
- `quota`: 账户额度（整数）
- 实际人民币余额 = quota / 500000

<p align="center">
  <small>© 2025 DMXAPI DMXAPI 用...</small>
</p>