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
        chunkSizeWarningLimit: 1000,
        cssCodeSplit: true,
        assetsInlineLimit: 4096, // 小于 4KB 的资源内联为 base64
        
        // 使用 esbuild 压缩（速度更快，无需额外安装）
        minify: 'esbuild',
        
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
            },
        },
    },
    
    // esbuild 配置（用于移除 console 和 debugger）
    esbuild: {
        drop: ['console', 'debugger'],
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
