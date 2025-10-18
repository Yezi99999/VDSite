const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
    transpileDependencies: true,
    outputDir: '../backend/static/frontend',// 指向Django的静态文件目录下的frontend子目录
    indexPath: '../../templates/frontend/index.html',  // 指向Django的模板目录下的frontend子目录
    // 设置静态资源路径（相对于outputDir）
    assetsDir: 'static',
    // 设置publicPath，根据环境变量来区分开发和生产
    publicPath: process.env.NODE_ENV === 'production' ? '/static/frontend/' : '/',
    devServer: {
    port: 8080, // 设置开发服务器端口
    host: 'localhost', // 或 '0.0.0.0' 允许外部访问
    open: true, // 启动时自动打开浏览器
        proxy: {
          // 配置 API 代理，解决跨域问题
        '/api': {
          target: 'http://localhost:8000', // Django 后端地址
          changeOrigin: true,
          pathRewrite: {
              '^/api': '/api' // 可以根据需要重写路径
          }
        }
      }
    },

})
