var path = require('path');

module.exports = {
  mode: 'development',
  entry: './src/background.js',
  output: {
    path: path.resolve(__dirname, './src/dist'),
    filename: 'background.bundle.js'
  }
};