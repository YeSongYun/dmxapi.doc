# Cursor 客户端配置、使用方法以及常见问题的解决方案

## 模型名称要使用改写
因为cursor发现模型名称里有Claude就会路由到官方URL造成报错，所以需要改模型名称，具体改写规则如下（仅供参考，以模型广场中cursor模块的实际名称为准）比如：

`DMXAPl-cls45-0929` 指向  claude-sonnet-4-5-20250929



::: warning
如果您想用cursor接入我们的模型，需要订阅pro会员，否则会报错，添加模型时，要打开vpn软件，否则没有添加模型的按键（添加完后关掉vpn），在使用cursor接DMXAPI的api时不要开vpn软件。
:::


## 详细的配置步骤

如果您是新手，可以参考下面的步骤进行配置，如果您已经有cursor客户端，可以直接跳过第一步，从第五步开始。

### 第一步
下载cursor客户端后，配置中文
![cursor](img/lag-1.png)

### 第二步
信任安装
![cursor](img/lag-2.jpg)

### 第三步
切换中文，重启cursor
![cursor](img/lag-3.jpg)

### 第四步（可选）
下载python插件，如果是新系统的话需要自己配置环境。

![cursor](img/lag-4.jpg)

### 第五步
开始准备接入DMXAPI的模型
![cursor](img/lag-5.jpg)

### 第六步
配置URL和key
![cursor](img/lag-6.png)

### 第七步
信任DMXAPI
![cursor](img/lag-7.jpg)

### 第八步
填写url的注意事项
![cursor](img/11-2.jpg)

### 第九步
打开模型列表，准备添加模型
![cursor](img/lag-9.jpg)

### 第十步
开始添加新模型
![cursor](img/lag-10.jpg)

### 第十一步
从网站找到模型名称，填写到cursor中
![cursor](img/lag-11.jpg)

### 第十二步
复制模型名称
![cursor](img/lag-12.jpg)

### 第十三步
粘贴到对应位置，完成模型添加
![cursor](img/lag-13.jpg)


### 第十四步
准备在对话框中切换模型
![cursor](img/lag-14.jpg)

### 第十五步
选中添加的模型
![cursor](img/lag-15.jpg)

### 第十六步
在文本框中输入文字内容，验证模型是否正常
![cursor](img/lag-16.jpg)




##  疑难杂症及解决方案

### 一、URL配置错误
url只能用下面图片中提体现的，不要修改，如果出下一下错误，说明您的url不对，需要将url改回为：https://www.dmxapi.cn/v1

![cursor](img/12-1.jpg)
### URL配置错误

### 1.URL配置错误返回错误码（到.cn结束）
![cursor](img/12-2.jpg)
### 2.URL配置错误返回错误码（到com/v1结束）
![cursor](img/12-3.jpg)

### 二、key配置错误
如果返回以下错误，说明您的key不对，需要确认一下有没有漏填或者复制错误的情况。
### 1.确认key跟填写的url是对应的
![cursor](img/12-31-1.jpg)
### 2.key配置错误返回错误码
![cursor](img/12-31-2.jpg)
<p align="center">
  <small>© 2025 DMXAPI Cursor配置</small>
</p>