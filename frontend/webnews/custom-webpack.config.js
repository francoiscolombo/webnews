const webpack = require('webpack');

module.exports = {
  plugins: [
    new webpack.DefinePlugin({
      $ENV: {
        BaseURL: JSON.stringify(process.env.WEBNEWS_API_BASE_URL),
        AppName: JSON.stringify(process.env.FRONTEND_APP_NAME),
        AppToken: JSON.stringify(process.env.FRONTEND_APP_TOKEN)
      }
    })
  ]
};
