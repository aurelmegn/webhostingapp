let Encore = require('@symfony/webpack-encore');
let PurgeCssPlugin = require('purgecss-webpack-plugin');
let glob = require('glob-all');
let path = require('path');

let collectWhitelistPatterns = _ => {
    return [
        /^bg-red-/,
        /^bg-green-/,
        /^bg-grey-/,
        /^bg-teal-/,
        /^bg-orange-/,
        
        /^text-red-/,
        /^text-green-/,
        /^text-grey-/,
        /^text-teal-/,
        /^text-orange-/,
        /^text-secondary-/,

        /^fa-info/,
        /^fa-times-circle/,
        /^fa-check-circle/,
        /^fa-exclamation-triangle/,
        /^fa-circle/,
    ]
}

Encore
    .setOutputPath('public')
    .setPublicPath('/public')
    .cleanupOutputBeforeBuild()

    .addEntry('js/app', './assets/js/index.js')
    .addEntry('js/dashboard', './assets/js/dashboard.js')

    .addStyleEntry('css/app', './assets/scss/index.scss')
    // .addStyleEntry('css/dashboard', './assets/scss/dashboard.scss')

    .enableSassLoader(function (options) { }, {
        resolveUrlLoader: false
    })

    // .enableSingleRuntimeChunk()

    .enablePostCssLoader(function (options) {
        options.config = {
            path: './assets/postcss.config.js'
        };
    })
    // .splitEntryChunks()
    .enableSingleRuntimeChunk()
    .enableBuildNotifications()
    .enableSourceMaps(!Encore.isProduction())
    .enableVersioning(Encore.isProduction())

;

if(Encore.isProduction()){
    Encore
        .addPlugin(new PurgeCssPlugin({
            paths: glob.sync([
                path.join(__dirname, 'templates/**/*.jinja')
            ]),
            extractors: [
                {
                    extractor: class {
                        static extract(content) {
                            return content.match(/[A-z0-9-:\/%]+/g) || []
                        }
                    },
                    extensions: ['jinja']
                }
            ],
            whitelistPatterns: collectWhitelistPatterns
        }))

}

module.exports = Encore.getWebpackConfig();
