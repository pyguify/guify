const HtmlWebpackPlugin = require('html-webpack-plugin')
const cheerio = require('cheerio')

module.exports = {
  entry: './src/index.js',

  plugins: [
    new HtmlWebpackPlugin({
      template: 'public/index.html',
      filename: 'index.html',
      inject: 'body',
      // Use a custom script to modify the contents of the template
      // before it is written to the output directory.
      minify: {
        removeComments: true,
        collapseWhitespace: true,
      },
      // The custom script that modifies the contents of the template.
      // In this example, we are adding a meta tag to the head section
      // of the template.
      scriptLoading: 'defer',
      scriptAttributes: {
        crossorigin: 'anonymous',
      },
      // ...
      // Other options for the HtmlWebpackPlugin
      // ...
      postProcessHtml: (html) => {
        const $ = cheerio.load(html)
        $('#eel-script').attr('src', '/eel.js')
        return $.html()
      },
    }),
  ],
}
