# Seedance 2.0 真人方案二 · 使用预置虚拟人像

Seedance 2.0 默认禁止上传真人脸。方案二直接用平台**预置的虚拟人像库**——里面全是 AI 生成的合规虚拟脸，免费、丰富。挑一个当「演员」即可生成视频，完全不碰真人、零合规风险。

适合需要真人风格的脸、但不指定具体某人的场景（带货口播、剧情演示、数字人主播等）；若必须用指定真人，请参考 [方案三 · 授权真人](./seedance-2-0-real-person-plan3-authorized-real-person.md)。

## 虚拟人像素材库

虚拟人像库在火山方舟**体验中心**里，每个虚拟形象就是一张图片，对应一个资产 ID（`asset ID`）。

:::tip 打开虚拟素材库
[火山方舟体验中心 · 虚拟人像库](https://console.volcengine.com/ark/region:ark+cn-beijing/experience/vision?modelId=doubao-seedance-2-0-260128&tab=GenVideo)

首次使用需先同意相关协议。
:::

## 用法三步

1. **挑人**：打开素材库，用自然语言描述或按性别 / 年龄 / 国籍筛选，选一个中意的虚拟人像。
2. **复制 asset ID**：在人像详情里复制它的资产 ID（形如 `asset-xxxxxxxx`）。
3. **引用**：生成视频时把它作为参考图传入，`url` 填 `asset://<asset ID>`，这张脸就会出镜；提示词里用「图片1 / 视频1」按素材顺序指代，别直接写 asset ID。

具体请求参数与调用方式，见 [doubao-seedance-2-0-260128 视频编辑](./doubao-seedance-2-0-260128-video-edit.md)或其他相关文档。

<p align="center">
  <small>© 2026 DMXAPI Seedance 2.0 真人方案二 使用预置虚拟人像</small>
</p>
