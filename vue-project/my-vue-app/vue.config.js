const { defineConfig } = require('@vue/cli-service');

// // 環境変数からAPIのドメインを取得
// const apiUrl = process.env.API_DOMAIN;
// const djangoApiUrl = process.env.DJANGO_API_DOMAIN;

module.exports = defineConfig({
  chainWebpack: (config) => {
    // Webpackの設定を変更するためのフック
    config.plugin('define').tap((definitions) => {
      // Vueプロダクションモード時のハイドレーションミスマッチの詳細を無効化
      definitions[0]['__VUE_PROD_HYDRATION_MISMATCH_DETAILS__'] = false;
      return definitions;
    });
  },
  // 依存関係のトランスパイルを有効にする
  transpileDependencies: true,
  devServer: {
    port: 3000, // 開発サーバーのポート番号
    // proxy: {
    //   // '/api'へのリクエストをAPIのURLにプロキシする設定
    //   '/api': {
    //     target: apiUrl, // プロキシ先のURL
    //     changeOrigin: true, // ヘッダーのHostをターゲットのURLに変更する
    //     pathRewrite: {
    //       '^/api': '' // リクエストのパスから'/api'を削除する
    //     }
    //   },
    //   // '/django-api'へのリクエストをDjango APIのURLにプロキシし、パスを修正する設定
    //   '/django-api': {
    //     target: djangoApiUrl, // プロキシ先のURL
    //     changeOrigin: true, // ヘッダーのHostをターゲットのURLに変更する
    //     pathRewrite: {
    //       '^/django-api': '/api' // リクエストのパスを修正する
    //     }
    //   },
    //   '/youtube_app': {
    //     target: djangoApiUrl, // プロキシ先のURL
    //     changeOrigin: true // ヘッダーのHostをターゲットのURLに変更する
    //   }
    // }
  }
});
