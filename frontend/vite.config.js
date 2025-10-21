import {fileURLToPath, URL} from 'node:url'

import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        vueDevTools(),
    ],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        },
    },
    envDir: '../', // Load .env files from the root directory
    
    // 构建优化配置
    build: {
        outDir: 'dist',
        sourcemap: false, // 不生成 sourcemap
        chunkSizeWarningLimit: Infinity, // 关闭 chunk 大小警告
        cssCodeSplit: true,
        assetsInlineLimit: 4096, // 小于 4KB 的资源内联为 base64
        
        // 使用 terser 进行深度压缩和混淆
        minify: 'terser',
        terserOptions: {
            compress: {
                // 移除 console
                drop_console: true,
                // 移除 debugger
                drop_debugger: true,
                // 移除所有注释
                passes: 2,
                // 移除未使用的代码
                dead_code: true,
                // 优化布尔值
                booleans: true,
                // 优化 if 返回和 continue
                if_return: true,
                // 合并连续变量声明
                join_vars: true,
                // 移除未引用的函数和变量
                unused: true,
            },
            mangle: {
                // 混淆顶级作用域变量名
                toplevel: true,
                // 混淆 eval 中的变量名
                eval: true,
                // 保留类名（避免某些框架出问题）
                keep_classnames: false,
                // 保留函数名（避免某些框架出问题）
                keep_fnames: false,
                // Safari 10 兼容
                safari10: true,
            },
            format: {
                // 移除所有注释
                comments: false,
                // 使用 ASCII 字符
                ascii_only: true,
            },
        },
        
        // Rollup 配置
        rollupOptions: {
            output: {
                // 代码分割 - 只包含实际使用的依赖
                manualChunks: {
                    'vue-vendor': ['vue', 'vue-router'],
                    'element-plus': ['element-plus'],
                    'element-icons': ['@element-plus/icons-vue'],
                    'axios': ['axios'],
                },
                // 文件命名
                chunkFileNames: 'js/[name]-[hash].js',
                entryFileNames: 'js/[name]-[hash].js',
                assetFileNames: (assetInfo) => {
                    const info = assetInfo.name.split('.')
                    const ext = info[info.length - 1]
                    if (/\.(png|jpe?g|gif|svg|ico|webp)$/i.test(assetInfo.name)) {
                        return 'img/[name]-[hash].[ext]'
                    }
                    if (/\.(woff2?|eot|ttf|otf)$/i.test(assetInfo.name)) {
                        return 'fonts/[name]-[hash].[ext]'
                    }
                    return 'assets/[name]-[hash].[ext]'
                },
                // 压缩输出
                compact: true,
            },
        },
        
        // 启用 CSS 压缩
        cssMinify: true,
        
        // 报告压缩后的大小
        reportCompressedSize: true,
        
        // 开启 Brotli 压缩（需要服务器支持）
        brotliSize: true,
    },
    
    // 依赖预构建 - 只包含实际使用的依赖
    optimizeDeps: {
        include: [
            'vue',
            'vue-router',
            'axios',
            'element-plus',
            '@element-plus/icons-vue',
        ],
    },
    
    // 开发服务器
    server: {
        port: 5173,
        open: true,
        proxy: {
            '/api': {
                target: 'http://localhost:8080',
                changeOrigin: true,
            },
        },
    },
})
