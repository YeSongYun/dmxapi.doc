// 1. 导入第三方主题
import Theme from '@escook/vitepress-theme'
// 2. 导入配套的 CSS 样式（此步骤不能省略）
import '@escook/vitepress-theme/style.css'
// 3. 引入 Viewer.js 的样式
import 'viewerjs/dist/viewer.css'

// 4. 扩展主题：使用 Viewer.js 作为图片查看器（支持滚轮缩放 & 弹窗）
export default {
  extends: Theme,
  enhanceApp({ router }: { router: any }) {
    if (typeof window === 'undefined') return

    let viewerInstance: any

    const initViewer = async () => {
      const { default: Viewer } = await import('viewerjs')

      // 销毁旧实例，避免重复绑定
      if (viewerInstance) {
        try { viewerInstance.destroy() } catch (e) {}
        viewerInstance = null
      }

      const container = document.querySelector('.vp-doc') as HTMLElement | null
      if (!container) return

      // 初始化 Viewer：点击图片弹窗展示，滚轮缩放
      viewerInstance = new Viewer(container, {
        inline: false,        // 使用弹窗模式
        navbar: false,        // 关闭缩略导航
        title: false,         // 不显示标题
        toolbar: true,        // 显示工具栏（缩放、旋转、重置等）
        tooltip: true,
        movable: true,
        zoomable: true,
        rotatable: false,
        scalable: false,
        transition: true,
        keyboard: true,
        zoomOnWheel: true,    // 鼠标滚轮缩放
        zoomRatio: 0.2,       // 每次滚轮缩放的比例
        zIndex: 10000,        // 提升弹层层级，避免被侧栏遮挡
        filter(image: Element) {
          // 仅选择 img，且排除带有 no-viewer 类名的图片
          return (
            image instanceof HTMLImageElement &&
            !image.classList.contains('no-viewer')
          )
        }
      })
    }

    // 首次进入 & 路由变更后都初始化
    initViewer()
    router.onAfterRouteChanged = () => initViewer()
  }
}