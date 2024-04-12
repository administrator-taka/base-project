const { defineConfig } = require('@vue/cli-service')

// 環境変数からAPIのドメインを取得
const apiUrl = process.env.API_DOMAIN
const djangoApiUrl = process.env.DJANGO_API_DOMAIN

module.exports = defineConfig({
  chainWebpack: (config) => {
    // Webpackの設定を変更するためのフック
    config.plugin('define').tap((definitions) => {
      // Vueプロダクションモード時のハイドレーションミスマッチの詳細を無効化
      definitions[0]['__VUE_PROD_HYDRATION_MISMATCH_DETAILS__'] = false
      return definitions
    })
  },
  // 依存関係のトランスパイルを有効にする
  transpileDependencies: true,
  configureWebpack: {
    // ファイルの変更を監視するオプション
    watchOptions: {
      aggregateTimeout: 300, // ファイル変更を検知してからビルドを開始するまでの遅延時間
      poll: 1000 // ファイルの変更を検知する間隔
    },
    resolve: {
      alias: {
        axios: 'axios' // axiosライブラリをエイリアスに設定
      }
    }
  },
  devServer: {
    port: 3000, // 開発サーバーのポート番号
    proxy: {
      // '/api'へのリクエストをAPIのURLにプロキシする設定
      '/api': {
        target: apiUrl, // プロキシ先のURL
        changeOrigin: true, // ヘッダーのHostをターゲットのURLに変更する
        pathRewrite: {
          '^/api': '' // リクエストのパスから'/api'を削除する
        }
      },
      // '/django-api'へのリクエストをDjango APIのURLにプロキシし、パスを修正する設定
      '/django-api': {
        target: djangoApiUrl, // プロキシ先のURL
        changeOrigin: true, // ヘッダーのHostをターゲットのURLに変更する
        pathRewrite: {
          '^/django-api': '/api' // リクエストのパスを修正する
        }
      }
    }
  }
})
