import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config

// 第三方主题：https://www.escook.cn/index.php/2024/05/06/escook-vitepress-theme-doc/

// 主题设置：https://vitepress.dev/reference/default-theme-config

export default defineConfig({
  //主题设置
  title: "DMXAPI 文档",
  description: "DMXAPI 大模型API接口使用教程文档",
  vite: {
    ssr: { noExternal: ['@escook/vitepress-theme', 'vitepress'] },
    build: {
      chunkSizeWarningLimit: 2048
    }
  }, //第三方主题生产HTML需要的设置

  appearance: 'dark', // 默认使用深色主题

  lastUpdated: true, // 启用文档最后更新时间显示

  themeConfig: {

    search: {
      provider: 'local'
    },
    siteTitle: 'DMXAPI',
    logo: '/D.png',
    lastUpdatedText: '最后更新',

    footer: {
      message: '一个 <span class="key-gradient">Key</span> 用全球大模型',
      copyright: 'Copyright © 2025 DMXAPI 版权所有'
    },

    //顶部菜单
    nav: [
      { text: '文档首页', link: '/' },
      { text: '联系我们', link: '/lianxi' },
      { text: '|', link: '' },
      { text: '📗更新', link: 'https://www.dmxapi.cn/weblog' },
      { text: '💰模型价格', link: 'https://www.dmxapi.cn/rmb' },
      { text: '🐍Claude Code', link: '/claude-code-new' },
      // { text: '🔧模型参数', link: 'http://models.dmxapi.cn/' },
      { text: '🎫开发票', link: 'https://www.dmxapi.cn/fapiao' },
      { text: '🗏 返回DMXAPI', link: 'https://dmxapi.cn' },
    ],

    //左侧导航
    sidebar: [
      {
        text: 'DMXAPI介绍',
        collapsed: true,
        items: [
          { text: 'DMXAPI介绍', link: '/about' },
          { text: '平台优势/特色', link: '/youshi' },
          { text: '使命·价值观', link: '/values' },
          { text: '团队介绍', link: '/teams' },
          { text: 'AI探索路', link: '/qiyuan' },
          // { text: '商务资料下载', link: '/pptpdf' },
        ],
      },
      {
        text: '平台管理接口',
        collapsed: true,
        items: [
          { text: '系统令牌&用户ID', link: '/security_token_ID' },
          { text: '余额查询', link: '/yuer' },
          { text: '模型列表', link: '/model-list' },
          { text: '模型统计', link: '/Model-statistics' },
          {
                text: '日志查询',
                collapsed: true,
                items: [
                  { text: '总消耗查询', link: '/log_query' },
                  { text: '消耗细化查询', link: '/log_query_all' }
                ],
          },
          {
                text: '令牌相关',
                collapsed: true,
                items: [
                  { text: '获取所有令牌', link: '/Get_all_tokens' },
                  { text: '搜索令牌', link: '/Search_token' },
                  { text: '创建令牌', link: '/Create_token' },
                  { text: '更新令牌', link: '/Update_token' },
                  { text: '批量删除令牌', link: '/Batch_token_deletion' },
                  { text: '令牌余额', link: '/key-yuer' },
                ],
          },
        ],
      },
      {
        text: 'API调用',
        collapsed: true,
        items: [
          { text: '欢迎使用', link: '/jichu' },
          {
            text: '快速入门 DMXAPI',
            collapsed: true,
            items: [
              { text: '快速开始', link: '/kaishi' },
              { text: '注册教程', link: '/ZC' },
              { text: '充值教程', link: '/CZ' },
              { text: '如何新建令牌Key', link: '/lingpai' },
              { text: '获得 Base url', link: '/baseurl' },
              { text: '支持官方SDK', link: '/sdk' },
             
              
              {
                text: '计费方式',
                collapsed: true,
                items: [
                  { text: '计费规则', link: '/jijia' },
                  { text: '豆包计费明细', link: '/usage-tokens' },
                  { text: 'vidu计费规则', link: '/viduJF' },
                ],
              },
              { text: '常见报错码', link: '/error-nub' },

              {
                text: '-thinking思考功能的开关',
                collapsed: true,
                items: [
                  { text: 'Claude 推理开关', link: '/thinking-claude' },
                  { text: 'Gemini 推理开关', link: '/thinking-gemini' },
                  { text: 'Qwen 千问推理开关', link: '/thinking-qwen' },
                  { text: 'Doubao 豆包推理开关', link: '/thinking-doubao' },
                ],
              },

               { text: 'DMXAPI 搜索模型选型指南', link: '/research' }
            ],
          },
          {
            text: 'Openai 请求格式（通用）',
            collapsed: true,
            items: [
              { text: '适用范围：♥ 所有模型', link: '/fanwei' },
              { text: '普通文本对话（非流）', link: '/openai-chat' },
              { text: '普通文本对话（流式输出）', link: '/openai-chat-stream' },
              { text: '固定格式化输出Json', link: '/openai-json' },
              { text: 'embedding代码例子', link: '/embedding' },
              { text: '视频分析（网络）', link: '/Qwen3-VL-235B-A22B-Thinking' },
              { text: '图片分析（网络）', link: '/url-image' },
              { text: '图片分析（本地）', link: '/base64-image'},
              { text: '函数调用FunctionCall', link: '/function-call' },
              { text: 'whisper-stt', link: '/opneai-stt' },
              { text: 'gpt-tts', link: '/openai-tts' },
              { text: 'gpt-5.2-pro', link: '/gpt-5.2-pro' },
              { text: 'openai绘图模型', link: '/gpt-image' },
              { text: 'openai多轮对话', link: '/gpt-5.4_Multi-turn-dialogue' }
            ],
          },
          {
            text: 'Openai 请求格式（新）',
            collapsed: true,
            items: [
              { text: 'Responses 接口介绍', link: '/responses' },
              { text: '普通文本对话（非流）', link: '/OpenAI_request_Text' },
              { text: '普通文本对话（流式输出）', link: '/res-chat-stream' },
              { text: '图片分析（网络）', link: '/res-url-image' },
              { text: '图片分析（本地）', link: '/res-base64-image' },
              { text: '文件分析', link: '/res-file' },
              { text: '函数调用FunctionCall', link: '/res-function-call' },
              { text: 'gpt思考内容', link: '/gpt-thinking' },
              { text: 'GPT-5.1 指南', link: '/GPT-5.1' },
              { text: 'GPT-5.2 指南', link: '/gpt-5.2' },
              { text: 'GPT-5.4 指南', link: '/GPT-5.4' },
              // { text: 'GPT-5.4 Computer Use', link: '/gpt-5.4_computer_use' },

            ],
          },
          {
            text: 'Gemini 请求格式',
            collapsed: true,
            items: [
              { text: '文本对话（非流输出）', link: '/gemini-chat' },
              { text: '文本对话（流式输出）', link: '/gemini-chat-stream' },
              { text: 'PDF分析', link: '/gemini-pdf' },
              { text: '视频分析（本地）', link: '/gemini-video'},
              { text: '音频分析（本地）', link: '/gemini-stt'},
              { text: '图片分析（本地）', link: '/gemini-image' },
              { text: '图片分析（网络）', link: '/gemini-image1' },
              { text: 'json输出', link: '/gemini-json' },
                { text: '多轮对话', link: '/duolunduihua' },
              { text: '联网搜索', link: '/gemini-internet' },
              { text: 'Gemini 3 开发者指南', link: '/gemini-3' },
              { text: 'Gemini 3 思考总结', link: '/gemini3-thinking-summary' },
              { text: '多模态向量化', link: '/gemini-embedding-2-preview' },
            ],
          },
          {
            text: 'Claude 请求格式',
            collapsed: true,
            items: [
              { text: '文本对话', link: '/claude-chat' },
              { text: '图片分析', link: '/claude-image' }, 
              { text: '函数调用', link: '/claude-fc' },
              { text: 'sdk使用', link: '/claude-sdk' },
              { text: '缓存创建', link: '/claude-hc' },
              { text: '联网搜索', link: '/claude-serch' },
              { text: 'claude agent sdk', link: '/claude_agent_sdk' },
              { text: 'Claude-Opus-4.7 使用指南', link: '/claude_opus_4_7' },
            ],
          },
          {
            text: '🎨绘图模型',
            collapsed: true,
            items: [
              {
                text: 'openai绘图模型',
                collapsed: true,
                items: [
                  {
                    text: 'gpt-image-1.5',
                    collapsed: true,
                    items: [
                      { text: '文生图', link: '/img-gpt-image-1' },
                      { text: '图片编辑', link: '/gpt-image-edit' }
                    ],
                  },
                  {
                    text: 'gpt-image-2',
                    collapsed: true,
                    items: [
                      { text: '文生图', link: '/gpt-image-2-text-to-image' },
                      { text: '图片编辑', link: '/gpt-image-2-image-edit' }
                    ],
                  }
                ],
              },
              {
                text: '豆包即梦绘图模型',
                collapsed: true,
                items: [
                  {
                    text: 'doubao-seedream-5.0-lite',
                    collapsed: true,
                    items: [
                      { text: '文生图', link: '/doubao-seedream-5.0-lite-t2i' },
                      { text: '图片编辑', link: '/doubao-seedream-5.0-lite-img-edit' },
                      { text: '多图融合', link: '/doubao-seedream-5.0-lite-Multi-image-fusion' },
                    ],
                  },
                  {
                    text: 'doubao-seedream-4-5-251128',
                    collapsed: true,
                    items: [
                      { text: '文生图', link: '/img-seedream-45-t2i' },
                      { text: '图生图', link: '/img-seedream-45-i2i' },
                      { text: '多图融合', link: '/img-seedream-45-images' },
                    ],
                  },
                  {
                    text: 'doubao-seedream-4-0-250828',
                    collapsed: true,
                    items: [
                      { text: '文生图', link: '/img-seedream-40-t2i' },
                      { text: '图生图', link: '/img-seedream-40-i2i' },
                      { text: '多图融合', link: '/img-seedream-40-images' },
                    ],
                  },
                ],
              },

              {
                text: 'Gemini绘图模型',
                collapsed: true,
                items: [
                  {
                text: 'gemini-3.1-flash-image-preview',
                collapsed: true,
                items: [
                  { text: '文生图', link: '/gemini-3.1-flash-image-preview' },
                  { text: '图片编辑', link: '/gemini-3.1-flash-image-preview-edit' },
                  { text: '多图融合', link: '/gemini-3.1-flash-image-preview-images' },
                  { text: '多轮对话改图', link: '/gemini-3.1-flash-image-preview-duolun' },
                ],
                },

                  {
                text: 'gemini-3-pro-image-preview',
                collapsed: true,
                items: [
                  { text: '文生图', link: '/img-3pro-t2i' },
                  { text: '图片编辑', link: '/img-3pro-edit' },
                  { text: '多图融合', link: '/img-3pro-images' },
                  { text: '多轮对话改图', link: '/img-3pro-duolun' },
                  { text: '返回格式变化的说明', link: '/gemini-3-pro-image-preview' }
                ],
                },
                 {
                text: 'gemini-2.5-flash-image',
                collapsed: true,
                items: [
                  { text: '文生图', link: '/img-25flash-t2i' },
                  { text: '图片编辑', link: '/img-25flash-edit' },
                  { text: '多图融合', link: '/img-25flash-images' },
                  { text: '多轮对话改图', link: '/img-25flash-duolun' },
                ],
                },
                  
                //    {
                // text: 'nano-banana-2',
                // collapsed: true,
                // items: [
                //   { text: '文生图', link: '/nano-banana-2-01' },
                //   { text: '图片编辑', link: '/nano-banana-2-02' },
                //   { text: '多图融合', link: '/nano-banana-2-03' },
                //   { text: 'Gemini image 香蕉多轮对话改图文档', link: '/duolun' },
                //   { text: 'cherry studio', link: '/nano-banana-2-cherry'}
                // ],
                // },
                 
                 
                ],
                
              },
              
              //  { text: '百度绘图模型', link: '/baidu'},

               
              // {
              //   text: 'Flux绘图模型',
              //   collapsed: true,
              //   items: [
              //     { text: 'flux-2-flex', link: '/flux-2-flex' },
              //     { text: 'flux-2-pro', link: '/flux-2-pro' },
              //   ],
              // },

              {
                text: '阿里万相绘图模型',
                collapsed: true,
                items: [
                  {
                    text: 'wan2.6-image',
                    collapsed: true,
                    items: [
                      { text: '文生图', link: '/wan2.6-t2i' },
                      { text: '图文混排', link: '/wan2.6-image-interleave' },
                      { text: '图片编辑', link: '/wan2.6-image-edit' },
                    ],
                  },
                  {
                    text: 'wan2.7-image',
                    collapsed: true,
                    items: [
                      { text: '文生图', link: '/wan2.7-image-text-to-image' },
                      { text: '图片编辑', link: '/wan2.7-image-image-editing' },
                      { text: '组图生成', link: '/wan2.7-image-group-generation' },
                      { text: '交互式编辑', link: '/wan2.7-image-interactive-edit' },
                    ],
                  },
                  {
                    text: 'wan2.7-image-pro',
                    collapsed: true,
                    items: [
                      { text: '文生图', link: '/wan2.7-image-pro-text-to-image' },
                      { text: '图片编辑', link: '/wan2.7-image-pro-image-editing' },
                      { text: '组图生成', link: '/wan2.7-image-pro-group-image-generation' },
                      { text: '交互式编辑', link: '/wan2.7-image-pro-interactive-edit' },
                    ],
                  },
                ],
              },

              {
                text: '千问绘图模型',
                collapsed: true,
                items: [
                  { text: 'qwen-image', link: '/img-qwen-image' },
                  { text: 'qwen-image-edit', link: '/img-qwen-image-edit' },
                  { text: 'qwen-image-max', link: '/qwen-image-max' },
                  { text: 'qwen-image-plus-2026-01-09', link: '/qwen-image-plus-2026-01-09' },
                  {
                    text: 'qwen-image-edit-max-2026-01-16',
                    collapsed: true,
                    items: [
                      { text: '图片编辑', link: '/qwen-image-edit-max-2026-01-16-img-edit' },
                      { text: '多图融合', link: '/qwen-image-edit-max-2026-01-16-mul' },
                    ],
                  },
                  {
                    text: 'qwen-image-edit-plus-20260226',
                    collapsed: true,
                    items: [
                      { text: '图片编辑', link: '/qwen-image-edit-plus-20260226-img-edit' },
                      { text: '多图融合', link: '/qwen-image-edit-plus-20260226-mul' },
                    ],
                  },
                  {
                    text: 'qwen-image-2.0',
                    collapsed: true,
                    items: [
                      { text: '文生图', link: '/qwen-image-2.0-text-to-image' },
                      { text: '图片编辑', link: '/qwen-image-2.0-image-editing' },
                      { text: '多图融合', link: '/qwen-image-2.0-multi-image-fusion' },
                    ],
                  },
                  {
                    text: 'qwen-image-2.0-pro',
                    collapsed: true,
                    items: [
                      { text: '文生图', link: '/qwen-image-2.0-pro-text-to-image' },
                      { text: '图片编辑', link: '/qwen-image-2.0-pro-image-edit' },
                      { text: '多图融合', link: '/qwen-image-2.0-pro-multi-image-fusion' },
                    ],
                  },
                ],
              },

              
            ],
          },
          {
            text: '🎥视频模型 video',
            collapsed: true,
            items: [
              {
                text: '豆包视频模型 ',
                collapsed: true,
                items: [
                  {
                    text: 'seedance 1.5',
                    collapsed: true,
                    items: [
                      { text: '文生视频', link: '/doubao-seedance-1-5-pro-responses01' },
                      { text: '图生视频', link: '/doubao-seedance-1-5-pro-responses02' },
                      { text: '首尾帧生成视频', link: '/doubao-seedance-1-5-pro-responses03' },
                    ],
                  },
                  {
                    text: 'seedance 2.0',
                    collapsed: true,
                    items: [
                      { text: '文生视频', link: '/doubao-seedance-2-0-text-to-video' },
                      { text: '首帧生视频', link: '/doubao-seedance-2-0-260128-first-frame-to-video' },
                      { text: '首尾帧生视频', link: '/doubao-seedance-2-0-first-last-frame-video' },
                      { text: '视频编辑', link: '/doubao-seedance-2-0-260128-video-edit' },
                      { text: '视频延长', link: '/doubao-seedance-2-0-video-extend' },
                      { text: '多模态参考生视频', link: '/doubao-seedance-2-0-multimodal-reference-video' }
                    ],
                  },
                  {
                    text: 'seedance 2.0-fast',
                    collapsed: true,
                    items: [
                      { text: '文生视频', link: '/doubao-seedance-2-0-fast-text-to-video' },
                      { text: '首帧生视频', link: '/doubao-seedance-2-0-fast-260128-first-frame-to-video' },
                      { text: '首尾帧生视频', link: '/doubao-seedance-2-0-fast-260128-first-last-frame' },
                      { text: '视频编辑', link: '/doubao-seedance-2-0-fast-260128-video-editing' },
                      { text: '视频延长', link: '/doubao-seedance-2-0-fast-260128-video-extend' },
                      { text: '多模态参考生视频', link: '/doubao-seedance-2-0-fast-260128-video' }
                    ],
                  },
                ],
              },
              {
                text: 'MiniMax 海螺视频 Hailuo ',
                collapsed: true,
                items: [
                  { text: '文生视频', link: '/hailuo-txt2video' },
                  { text: '图生视频', link: '/hailuo-img2video' },
                  { text: '首尾帧生成视频', link: '/hailuo-task' }
                ],
              },

              //  {
              //   text: 'Sora视频模型',
              //   collapsed: true,
              //   items: [
              
              //     { text: 'sora2文生视频', link: '/sora2_t2v' },
              //     { text: 'sora2-pro文生视频', link: '/sora2-pro_t2v' },
              //   ],
              // },
// 
              // {
              //   text: 'Veo视频模型',
              //   collapsed: true,
              //   items: [
              
              //     { text: 'veo-3.1-fast-generate-preview文生视频', link: '/veo-3.1-fast-generate-preview' },
              //     { text: 'veo-3.1-generate-preview文生视频', link: '/veo-3.1-generate-preview' },
              //   ],
              // },

               {
                text: 'Vidu视频模型',
                collapsed: true,
                items: [
                  // { text: 'viduq2-pro（首尾帧）', link: '/viduq2-pro' },
                  // { text: 'viduq2（多图参考）', link: '/vidu-ptv' },
                  {
                    text: 'viduq2-pro',
                    collapsed: true,
                    items: [
                      { text: '首尾帧', link: '/viduq2-pro' },
                      { text: '多图参考', link: '/vidu-ptv' },
                    ],
                  },
                  {
                    text: 'viduq3-pro',
                    collapsed: true,
                    items: [
                      { text: '文生视频', link: '/viduq3-pro-text-to-video' },
                      { text: '图生视频', link: '/viduq3-pro-image-to-video' },
                      { text: '首尾帧生视频', link: '/viduq3-pro-start-end-to-video' },
                      
                    ],
                  },
                
                ],
              },
               
               {
                text: '拍我 视频模型 ',
                collapsed: true,
                items: [
                  { text: '图片上传', link: '/paiwo_image_upload' },
                  { text: '音频上传', link: '/paiwo-audio-upload' },
                  { text: '视频上传', link: '/paiwo-video-upload' },
                  {
                    text: 'paiwo-v5.6',
                    collapsed: true,
                    items: [
                      { text: '文生视频', link: '/paiwo-v5.6-ttv' },
                      { text: '图生视频', link: '/paiwo-v5.6-itv' },
                      { text: '首尾帧生成视频', link: '/paiwo-v5.6-itv2' },
                    ],
                  },
                  {
                    text: 'paiwo-v6',
                    collapsed: true,
                    items: [
                      { text: '文生视频', link: '/pixverse-v6-text-to-video' },
                      { text: '图生视频', link: '/pixverse-v6-img-to-video' },
                      { text: '首尾帧生成视频', link: '/pixverse-v6-first-last-frame' },
                      { text: '视频延长', link: '/pixverse-v6-video-extend' },
                    ],
                  },
                  {
                    text: 'PixVerse-C1',
                    collapsed: true,
                    items: [
                      { text: '文生视频', link: '/PixVerse-C1-text-to-video' },
                      { text: '图生视频', link: '/PixVerse-C1-image-to-video' },
                      { text: '首尾帧生成视频', link: '/PixVerse-C1-first-last-frame-to-video' },
                      { text: '参考生视频', link: '/PixVerse-C1-reference-to-video' },
                    ],
                  },
                  { text: '数字人 Lipsync', link: '/paiwo-itv-hd-lipsync' },

                ],
              },


               {
                text: 'Kling 视频模型 ',
                collapsed: true,
                items: [
                  { text: 'kling-v3-video-generation 文生视频', link: '/kling-v3-video-generation-t2v' },
                  { text: 'kling-v3-video-generation 文生视频（智能分镜）', link: '/kling-v3-video-generation-text-to-video' },
                  { text: 'kling-v3-video-generation 首帧生视频', link: '/kling-v3-video-generation-first-frame-to-video' },
                  { text: 'kling-v3-video-generation 首尾帧生视频', link: '/kling-v3-video-generation-first-last-frame' },
                  // { text: 'kling-v2-6-text2video', link: '/kling-v2-6-text2video' },
                  // { text: 'kling-v2-6-image2video', link: '/kling-v2-6-image2video'}
                ],
              },
              

              {
                text: '阿里万相视频模型',
                collapsed: true,
                items: [
              {
                text: 'wan2.6',
                collapsed: true,
                items: [
                  { text: '文生视频', link: '/wan2.6-t2v' },
                  { text: '首帧生视频', link: '/wan2.6-i2v' },
                  // { text: '参考生视频', link: '/wan2.6-r2v' }
                ],
              },
            ],
          },

              {
                text: '阿里 快乐马视频模型',
                collapsed: true,
                items: [
                  { text: '文生视频', link: '/happyhorse-1.0-t2v-text-to-video' },
                  { text: '首帧生视频', link: '/happyhorse-1.0-i2v-image-to-video' },
                  { text: '参考生视频', link: '/happyhorse-1.0-r2v-reference-to-video' },
                  { text: '视频编辑', link: '/happyhorse-1.0-video-edit-video-editing' },
                ],
              },

              { text: '更多视频模型正在赶来...', link: '/video-more' },
            ],
          },
          {
            text: '🔊️音频模型 TTS & STT',
            collapsed: true,
            items: [
              { text: 'TTS模型Gemini系列', link: '/gemini-2.5-pro-preview-tts' },
              { text: 'TTS模型 MinMax-speech', link: '/minimax-speech' },
              // { text: 'STT模型 whisper', link: '/opneai-stt' },
              { text: 'TTS模型 mimo-v2-tts', link: '/mimo-v2-tts' },
              { text: 'STT模型 gpt-4o-transcribe', link: '/gpt-4o-transcribe' },
              { text: 'STT模型 Qwen3-Omni-Captioner', link: '/Qwen3-Omni-Captioner' },
              
              {
                text: 'Minimax 声音克隆 ',
                collapsed: true,
                items: [
                  { text: '音频文件上传', link: '/minimax-clone' },
                  { text: '声音克隆', link: '/minimax-clone-lastversion' },
                  { text: '同步语音合成', link: '/speech-2.8-hd' },
                ],
              },
            ],
          },

          {
            text: '🎵音乐模型',
            collapsed: true,
            items: [
              {
                text: 'suno-music',
                collapsed: true,
                items: [
                  { text: 'suno音乐生成', link: '/suno-music-all' },
                  // { text: 'chirp-v5使用指南', link: '/suno-music' }
             
                  
                ],
              },

              {
                text: 'MiniMax-music',
                collapsed: true,
                items: [
                  { text: 'music-2.0', link: '/music-2.0' },
                  {
                    text: 'music-2.5',
                    collapsed: true,
                    items: [
                      { text: 'music-2.5非流式输出', link: '/music-2.5-feiliushi' },
                      { text: 'music-2.5流式输出', link: '/music-2.5-liushi' }
                      
                    ],
                  }
                ],
              },
            ],
          },


          {
            text: '📚RAG-向量/重排序',
            collapsed: true,
            items: [
              { text: 'jina-reranker', link: '/rerank-jina-reranker' },
              // { text: 'qwen3-reranker-8b', link: '/rerank-qwen3-reranker-8b' },
              { text: 'bge-reranker-v2-m3-free', link: '/rerank-bge-reranker-v2-m3' },
              { text: 'doubao-embedding-large-text', link: '/emb-doubao-embedding-large-text' },
              { text: '阿里 text-embedding-v4', link: '/emb-text-embedding-v4' },
              { text: 'OpenAi 向量模型', link: '/embedding' },
              { text: 'doubao-embedding-vision-251215', link: '/doubao-embedding-vision-251215' },
              { text: 'gemini-embedding-2-preview', link: '/gemini-embedding-2-preview' },
            ],
          },
          

         {
            text: '🌐翻译模型',
            collapsed: true,
            items: [
              { text: 'Qwen-MT系列翻译模型', link: '/Qwen-MT' },
             
            ],
          },

          {
            text: '🔍搜索模型',
            collapsed: true,
            items: [
              {
                text: 'Perplexity Sonar 系列 ',
                collapsed: true,
                items: [
                  { text: 'perplexity-deep-research-ssvip', link: '/perplexity-deep-research-ssvip' },
                  { text: 'perplexity-sonar-pro-ssvip', link: '/perplexity-sonar-pro-ssvip' },
                  { text: 'perplexity-sonar-reasoning-pro-ssvip', link: '/perplexity-sonar-reasoning-pro-ssvip' },
                  { text: 'perplexity-sonar-pro-search-ssvip', link: '/perplexity-sonar-pro-search-ssvip' },
                  { text: 'perplexity-sonar-ssvip', link: '/perplexity-sonar-ssvip' },
                ],
              },
             
            ],
          },


         {
            text: '🚀全模态模型',
            collapsed: true,
            items: [
              { text: 'qwen3-omni-flash全模态模型', link: '/qwen3-omni-flash' },
              {
                text: 'mimo-v2-omni全模态模型 ',
                collapsed: true,
                items: [
                  { text: '视频分析', link: '/mimo-v2-omni-Video_understanding' },
                  { text: '图片分析', link: '/mimo-v2-omni-pic_understanding' },
                  { text: '音频分析', link: '/mimo-v2-omni-Audio_understanding' },
                ],
              },
              {
                text: 'qwen3.5-omni-plus-all全模态模型',
                collapsed: true,
                items: [
                  { text: '文 生 文+音频', link: '/qwen3.5-omni-plus-all-text-to-text-audio' },
                  { text: '文+音频 生 文+音频', link: '/qwen3.5-omni-plus-all-text-audio-to-text-audio' },
                  { text: '文+本地音频 生 文+音频', link: '/qwen3.5-omni-plus-all-audio-to-text-audio' },
                  { text: '文本+本地图片 生 文本+音频', link: '/qwen3.5-omni-plus-all-local-image-to-text-audio' },
                  { text: '文+图 生 文+音频', link: '/qwen3.5-omni-plus-all-text-image-to-text-audio' },
                  { text: '文+视频 生 文+音频', link: '/qwen3.5-omni-plus-all-video-text-to-text-audio' },
                  { text: '文本+本地视频 生 文本+音频', link: '/qwen3.5-omni-plus-all-video-to-text-audio' },
                  { text: '多轮对话', link: '/qwen3.5-omni-plus-all-multi-turn-dialog' },
                  { text: '多模态组合输入', link: '/qwen3.5-omni-plus-all-multimodal-combined' },
                ],
              },

            ],
          },



          {
            text: '数据处理（文档/PDF/OCR）',
            collapsed: true,
            items: [
              { text: 'deepseek-ocr', link: '/deepseek-ocr' },
              { text: 'qwen-vl-ocr-latest', link: '/qwen-vl-ocr-latest' },
              { text: 'somark', link: '/somark' },
              { text: '合合文档解析模型', link: '/hehe' }
              
            ],
          },

          {
            text: '其他示例',
            collapsed: true,
            items: [
              { text: 'LangChain', link: '/langchain' },
              { text: 'qwen-deep-research', link: '/qwen-deep-research' },
              { text: '界面交互模型gui-plus', link: '/gui-plus' },
              { text: 'qwen-plus-character角色扮演模型', link: '/qwen-plus-character' },
              { text: 'qwen3-max-2026-01-23', link: '/qwen3-max-2026-01-23' },
              {
                text: 'M2-her',
                collapsed: true,
                items: [
                  { text: '普通对话', link: '/m2-her-nc' },
                  { text: '多轮对话', link: '/m2-her_multi-dia' },
                ],
              },
            ],
          },

  
        ]
      },
      {
        text: '各类第三方应用配置',
        collapsed: true,
        items: [

          // { text: 'Claude code(推荐)', link: '/claude-code' },
          { text: 'Claude code(推荐)', link: '/claude-code-new' },
          { text: 'cc switch配置codex', link: '/cc_switch' },
          // { text: 'cc switch配置claude code', link: '/cc_switch_to_claude code' },
          { text: 'Qwen3 coder', link: '/qwen-coder' },
          { text: 'Openai Codex', link: '/codex' },
          { text: 'opencode', link: '/opencode' },
          { text: 'Cherry Studio', link: '/cherry-studio' },
          { text: 'Cherry Studio调用gpt-5.2-pro', link: '/cherry-studio-gpt-5.2-pro' },
          { text: 'Cherry Studio调用 Perplexity Sonar 系列搜索模型', link: '/cherry_perplexity' },
          { text: 'Cherry Studio 使用 Gemini 模型联网搜索', link: '/cherry_gemini_web' },
          { text: 'Chatwise', link: '/chatwise' },
          { text: 'chatbox', link: '/chatbox' },
          { text: 'Dify', link: '/dify' },
          { text: 'coze', link: '/coze-llm-plug' },
          { text: 'VSCode CLine', link: '/Cline' },
          { text: 'n8n', link: '/n8n' },
          { text: 'Cursor', link: '/cursor' },
          { text: 'ONLYOFFICE', link: '/onlyoffice' },
          { text: 'Roo_Code', link: '/roo_code' },
          { text: 'AnythingLLM', link: '/AnythingLLM' },
          { text: '思源笔记', link: '/siyuanbiji' },
          { text: 'Typing Mind', link: '/typingmind' },
          { text: '提示词优化器', link: '/prompt-optimizer' },
          // { text: 'GitHub Copilot', link: '/GitHub Copilot' },
          { text: 'OpenClaw官方版配置DMXAPI', link: '/openclaw_config' },
          { text: 'OpenClaw(DMXAPI汉化版)', link: '/clawdbot' },
          { text: '沉浸式翻译', link: '/chenjinshifanyi' },
          { text: 'fluentread', link: '/fluentread' },
          { text: 'workbuddy', link: '/workbuddy' },
          { text: 'codebuddy', link: '/codebuddy' },
          { text: '腾讯云openclaw', link: '/Tencent_openclaw' },
          { text: 'Trae', link: '/Trae' },
          // { text: 'Claude-Desktop', link: '/claude_code_desktop' },
          { text: 'pi_agent', link: '/pi_agent' },
          { text: 'kilo_code', link: '/kilo_code' },
          { text: 'hermes_agent', link: '/hermes_agent' },
        ],
      },
      {
        text: '服务条款',
        items: [
          { text: '隐私条款', link: '/tiaokuan' },
          { text: '服务承诺', link: '/chengnuo' },
          { text: '帮助中心', link: '/help-center' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/vuejs/vitepress' } 
    ]
  }
})
