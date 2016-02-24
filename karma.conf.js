// Karma configuration
// Generated on Mon Dec 14 2015 09:19:42 GMT-0800 (PST)

module.exports = function (config) {
    config.set({

        // base path that will be used to resolve all patterns (eg. files, exclude)
        basePath: '',


        // frameworks to use
        // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
        frameworks: ['jasmine', 'angular-filesort'],


        angularFilesort: {
          whitelist: [
            '**/static/**/*.js'
          ]
        },


        // list of files / patterns to load in the browser
        files: [
            'build/js/angular.js',
            'build/js/angular-mocks.js',
            'build/js/jQuery.js',
            '**/static/**/*.js',
            'static/**/*.html'
        ],

        // list of files to exclude
        exclude: [
            'static/**/*.js', 'venv/**', 'node_modules/**/static/**'
        ],


        // preprocess matching files before serving them to the browser
        // available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
        preprocessors: {
            '**/static/**/*.js': ['coverage'],
            'static/**/*.html': ['ng-html2js']
        },


        // test results reporter to use
        // possible values: 'dots', 'progress'
        // available reporters: https://npmjs.org/browse/keyword/karma-reporter
        reporters: ['progress', 'coverage'],


        // web server port
        port: 9876,


        // enable / disable colors in the output (reporters and logs)
        colors: true,


        // level of logging
        // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
        logLevel: config.LOG_INFO,


        // enable / disable watching file and executing tests whenever any file changes
        autoWatch: false,


        // start these browsers
        // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
        browsers: ['PhantomJS'],

        // Continuous Integration mode
        // if true, Karma captures browsers, runs the tests and exits
        singleRun: true,

        // Concurrency level
        // how many browser should be started simultanous
        concurrency: Infinity,

        browserDisconnectTimeout: 5000,
        browserNoActivityTimeout: 10000,
        browserDisconnectTolerance: 10,

        coverageReporter: {
            type: 'html',
            dir: 'coverage/',
            check: {
                each: {
                    statements: 90,
                    branches: 0,
                    functions: 90,
                    lines: 90
                }
            }
        },

        ngHtml2JsPreprocessor: {
            prependPrefix: '/',
            moduleName: 'staticNgTemplates'
        },
    })
};
