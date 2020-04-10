var path = require('path');

module.exports = {
  mode: 'development',
  entry: './src/content.js',
  output: {
    path: path.resolve(__dirname, './src/dist'),
    filename: 'content.bundle.js'
  }
};