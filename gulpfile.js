// Include gulp
var gulp = require('gulp');

// Include Our Plugins
var jshint = require('gulp-jshint');

var scripts = ['**/static/**/*.js',
    '!static/**', '!venv/**', '!node_modules/**'];

var assets = require('./assets.json');

gulp.task('lint', function() {
    return gulp.src(scripts)
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
});

gulp.task('copy-js-assets', function() {
   return gulp.src(assets.js)
       .pipe(gulp.dest('./build/js'));
});

gulp.task('copy-css-assets', function() {
   return gulp.src(assets.css)
       .pipe(gulp.dest('./build/css'));
});

gulp.task('default', ['lint', 'copy-js-assets', 'copy-css-assets']);
