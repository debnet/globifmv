var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
const { VueLoaderPlugin } = require('vue-loader');

module.exports = {
    context: __dirname,
    entry: './assets/js/index',
    mode: 'development',
    output: {
        path: path.resolve('./static/'),
        filename: 'app.js'
    },

    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),
        new VueLoaderPlugin(),
        new webpack.HotModuleReplacementPlugin()
    ],

    module: {
        rules: [
            {
                test: /\.js$/,
                loader: 'babel-loader',
                include: [
                  path.resolve('assets'),
                  path.resolve('node_modules/vue-awesome')
                ]
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            {
                test: /\.css$/,
                use: [
                  'style-loader',
                  'css-loader'
                ]
            },
            {
              test: /\.(png|svg|jpg|gif)$/,
              use: [
                  {
                      loader: 'file-loader',
                      options: {
                        name: 'img/[name].[ext]',
                        publicPath: 'static'
                      }
                  }
              ]
            }
        ],
    },
    resolve: {
        alias: {
            vue: 'vue/dist/vue.js',
            '_STATIC_': path.resolve('static')
        }
    },

};