const { defineConfig } = require('@vue/cli-service')
const apiUrl = process.env.API_DOMAIN
const djangoApiUrl = process.env.DJANGO_API_DOMAIN

module.exports = defineConfig({
  chainWebpack: (config) => {
    config.plugin('define').tap((definitions) => {
      definitions[0]['__VUE_PROD_HYDRATION_MISMATCH_DETAILS__'] = false
      return definitions
    })
  },
  transpileDependencies: true,
  configureWebpack: {
    resolve: {
      alias: {
        axios: 'axios'
      }
    }
  },
  devServer: {
    port: 3000,
    proxy: {
      '/api': {
        target: apiUrl,
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''
        }
      },
      '/django-api': {
        target: djangoApiUrl,
        changeOrigin: true,
        pathRewrite: {
          '^/django-api': '/api'
        }
      }
    }
  }
})
