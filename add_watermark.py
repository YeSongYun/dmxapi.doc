"""
DMXAPI 图片水印批量处理工具

本脚本用于批量为指定的图片文件添加 DMXAPI 品牌水印。
主要功能包括：
1. 支持多种水印位置（右下角、左下角、右上角、左上角、居中）
2. 可调节水印透明度和大小比例
3. 批量处理多个图片文件
4. 自动检查文件存在性并提供处理结果反馈
5. 直接替换原始文件，节省存储空间

技术特点：
- 使用 PIL (Pillow) 库进行图像处理
- 支持 RGBA 透明通道处理
- 采用高质量的 LANCZOS 重采样算法
- 错误处理机制完善，确保程序稳定运行

作者: DMXAPI 团队
版本: 1.0
创建日期: 2025年
"""

from PIL import Image, ImageEnhance  # PIL库用于图像处理和增强
import os  # 系统操作库，用于文件路径处理
       

def add_watermark(image_path: str, watermark_path: str, output_path: str, position: str = 'bottom-right', opacity: float = 0.7, scale: float = 0.15) -> bool:
    """
    为单张图片添加水印的核心函数
    
    本函数实现了完整的水印添加流程，包括图片加载、水印缩放、透明度调整、
    位置计算、图层合成等步骤。支持多种自定义参数以满足不同的水印需求。
    
    参数说明:
        image_path (str): 原始图片的完整文件路径
                         支持常见图片格式（PNG、JPG、JPEG、BMP等）
        watermark_path (str): 水印图片的完整文件路径
                             建议使用PNG格式以支持透明背景
        output_path (str): 输出图片的保存路径
                          可以与原图路径相同以实现覆盖
        position (str): 水印在图片中的位置，支持以下选项：
                       - 'bottom-right': 右下角（默认）
                       - 'bottom-left': 左下角
                       - 'top-right': 右上角  
                       - 'top-left': 左上角
                       - 'center': 居中显示
        opacity (float): 水印的透明度，取值范围 0.0-1.0
                        0.0 = 完全透明，1.0 = 完全不透明
                        默认值 0.7 提供良好的可见性和美观度
        scale (float): 水印相对于原图的缩放比例
                      0.15 表示水印宽度为原图宽度的15%
                      高度按比例自动计算以保持水印原始宽高比
    
    返回值:
        bool: 处理成功返回 True，失败返回 False
    
    异常处理:
        捕获所有可能的异常（文件不存在、格式不支持、内存不足等）
        并输出详细的错误信息，确保程序不会因单个文件错误而崩溃
    """
    try:
        # 第一步：加载图片文件并转换为RGBA模式
        # RGBA模式包含红、绿、蓝、透明度四个通道，支持透明效果处理
        base_image = Image.open(image_path).convert('RGBA')
        watermark = Image.open(watermark_path).convert('RGBA')
        
        # 第二步：计算水印的目标尺寸
        # 获取原图的宽度和高度（像素单位）
        base_width, base_height = base_image.size
        
        # 根据缩放比例计算水印的目标宽度
        watermark_width = int(base_width * scale)
        
        # 按照水印原始宽高比计算目标高度，保持水印不变形
        # 公式：新高度 = 原高度 × (新宽度 / 原宽度)
        watermark_height = int(watermark.size[1] * (watermark_width / watermark.size[0]))
        
        # 第三步：调整水印大小
        # 使用LANCZOS重采样算法，提供最佳的缩放质量
        # LANCZOS算法在缩放时能更好地保持图像细节和边缘清晰度
        watermark = watermark.resize((watermark_width, watermark_height), Image.Resampling.LANCZOS)
        
        # 第四步：调整水印透明度
        if opacity < 1.0:
            # 提取水印的Alpha通道（透明度通道）
            alpha = watermark.split()[3]
            
            # 使用ImageEnhance.Brightness调整Alpha通道的亮度
            # 亮度值小于1.0会增加透明度，大于1.0会减少透明度
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
            
            # 将调整后的Alpha通道重新应用到水印图片
            watermark.putalpha(alpha)
        
        # 第五步：根据指定位置计算水印的坐标
        margin = 20  # 水印与图片边缘的距离（像素）
        
        if position == 'bottom-right':
            # 右下角：从右边缘和底边缘分别减去水印尺寸和边距
            x = base_width - watermark_width - margin
            y = base_height - watermark_height - margin
        elif position == 'bottom-left':
            # 左下角：左边距固定，底部位置计算同右下角
            x = margin
            y = base_height - watermark_height - margin
        elif position == 'top-right':
            # 右上角：右边位置计算同右下角，顶部边距固定
            x = base_width - watermark_width - margin
            y = margin
        elif position == 'top-left':
            # 左上角：左边距和顶部边距都固定
            x = margin
            y = margin
        elif position == 'center':
            # 居中：计算水印在水平和垂直方向的中心位置
            x = (base_width - watermark_width) // 2
            y = (base_height - watermark_height) // 2
        else:
            # 默认情况：如果位置参数无效，使用右下角
            x = base_width - watermark_width - margin
            y = base_height - watermark_height - margin
        
        # 第六步：创建透明图层并放置水印
        # 创建一个与原图相同尺寸的完全透明图层
        transparent = Image.new('RGBA', base_image.size, (0, 0, 0, 0))
        
        # 将调整好的水印粘贴到透明图层的指定位置
        transparent.paste(watermark, (x, y))
        
        # 第七步：合成最终图片
        # 使用alpha_composite方法将原图和水印图层进行Alpha混合
        # 这种方法能正确处理透明度，产生自然的水印效果
        watermarked = Image.alpha_composite(base_image, transparent)
        
        # 第八步：保存处理后的图片
        # 转换为RGB模式以兼容更多输出格式（某些格式不支持Alpha通道）
        watermarked = watermarked.convert('RGB')
        
        # 保存为PNG格式，quality=95确保高质量输出
        # PNG格式能很好地保持图片质量，适合包含文字和图形的水印
        watermarked.save(output_path, 'PNG', quality=95)
        
        # 输出成功信息，显示处理的文件名（不包含路径）
        print(f"✓ 成功为 {os.path.basename(image_path)} 添加水印")
        return True
        
    except Exception as e:
        # 异常处理：捕获并显示详细错误信息
        # 常见错误包括：文件不存在、格式不支持、权限不足、内存不足等
        print(f"✗ 处理 {os.path.basename(image_path)} 时出错: {str(e)}")
        return False


def main() -> None:
    """
    主函数 - 批量水印处理的控制中心
    
    本函数负责整个批量处理流程的协调和管理，包括：
    1. 初始化文件路径和配置参数
    2. 验证必要文件的存在性
    3. 遍历目标图片列表并逐一处理
    4. 统计处理结果并输出汇总信息
    5. 提供用户友好的进度反馈
    
    处理流程：
    - 设置工作目录和文件路径
    - 检查水印文件是否存在
    - 批量处理指定的图片文件
    - 统计成功和失败的数量
    - 输出最终处理报告
    """
    
    # 第一步：初始化文件路径配置
    # 获取当前脚本文件的绝对路径，确保路径计算的准确性
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 构建图片目录路径（脚本同级的img文件夹）
    img_dir = os.path.join(base_dir, 'img')
    
    # 构建水印文件的完整路径
    # DMXAPI-logo2.png 是预设的品牌水印图片
    watermark_path = os.path.join(img_dir, 'DMXAPI-logo2.png')
    
    # 第二步：定义需要处理的图片文件列表
    # 填写相对于脚本所在目录的路径，例如 'img\\ruanzhu.png'
    # 可以根据实际需要修改这个列表
    image_files = [
                'img/fanyi01.png',
                'img/fanyi02.png',
                'img/fanyi03.png',
                'img/fanyi04.png',
                'img/fanyi05.png'
    ]               
    
    # 第三步：验证水印文件存在性
    # 如果水印文件不存在，整个处理流程无法进行
    if not os.path.exists(watermark_path):
        print(f"错误: 水印文件不存在: {watermark_path}")
        print("请确保 DMXAPI-logo2.png 文件位于 img 目录中")
        return  # 提前退出函数
    
    # 第四步：输出处理开始信息
    print("=" * 60)
    print("🚀 DMXAPI 图片水印批量处理工具")
    print("=" * 60)
    print(f"📁 工作目录: {base_dir}")
    print(f"🖼️  图片目录: {img_dir}")
    print(f"🏷️  水印文件: {os.path.basename(watermark_path)}")
    print(f"📋 待处理文件数量: {len(image_files)}")
    print("-" * 60)
    
    # 第五步：初始化统计变量
    success_count = 0  # 成功处理的文件数量
    total_count = len(image_files)  # 总文件数量
    
    # 第六步：批量处理图片文件
    # 遍历图片文件列表，逐一进行水印添加处理
    for index, image_file in enumerate(image_files, 1):
        # 构建当前图片的完整路径（相对于脚本目录）
        image_path = os.path.join(base_dir, image_file)
        
        # 显示当前处理进度
        print(f"[{index}/{total_count}] 正在处理: {image_file}")
        
        # 检查原图文件是否存在
        if not os.path.exists(image_path):
            print(f"    ⚠️  跳过不存在的文件: {image_file}")
            continue  # 跳过当前文件，继续处理下一个
        
        # 设置输出路径（直接覆盖原始文件）
        # 这样可以节省存储空间，但建议在处理前备份重要文件
        output_path = image_path
        
        # 调用水印添加函数进行处理
        # 使用精心调优的参数设置：
        # - position='bottom-right': 水印位置在右下角，不影响主要内容
        # - opacity=0.3: 30%的不透明度，既保证可见性又不过于突兀
        # - scale=0.12: 水印大小为原图宽度的12%，大小适中
        if add_watermark(
            image_path=image_path,
            watermark_path=watermark_path,
            output_path=output_path,
            position='bottom-right',  # 右下角位置，符合常见水印习惯
            opacity=0.5,              # 50%透明度，平衡可见性和美观性
            scale=0.12                # 12%缩放比例，确保水印不会过大
        ):
            success_count += 1  # 成功计数器递增
            print(f"    ✅ 处理完成")
        else:
            print(f"    ❌ 处理失败")
    
    # 第七步：输出最终处理报告
    print("-" * 60)
    print("📊 处理结果统计:")
    print(f"   ✅ 成功处理: {success_count} 个文件")
    print(f"   ❌ 处理失败: {total_count - success_count} 个文件")
    print(f"   📈 成功率: {(success_count/total_count*100):.1f}%")
    print("=" * 60)
    
    # 根据处理结果输出相应的提示信息
    if success_count > 0:
        print("🎉 水印添加完成啦！")
        print("💡 提示: 原始图片已被替换为带水印的版本")
        print("📝 建议: 如需保留原图，请提前备份文件")
    else:
        print("😞 没有文件被成功处理")
        print("🔍 请检查文件路径和权限设置")
    
    print("=" * 60)


# 程序入口点
# 当脚本被直接运行时（而不是被导入时），执行main函数
if __name__ == "__main__":
    main()