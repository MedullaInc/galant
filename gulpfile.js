// Include gulp
var gulp = require('gulp');

// Include Our Plugins
var jshint = require('gulp-jshint');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');
var del = require('del');
var Server = require('karma').Server;
var watch = require('gulp-watch');

var scripts = ['**/static/**/*.js',
    '!**/static/**/*test*.js', '!static/**', '!venv/**', '!node_modules/**'];

var tests = ['**/static/**/*test*.js',
    '!static/**', '!venv/**', '!node_modules/**'];

var assets = require('./assets.json');

var outdir = 'build';
var jsout = outdir + '/js';
var cssout = outdir + '/css';

gulp.task('lint', function () {
    return gulp.src(scripts)
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
});

gulp.task('copy-js-assets', function () {
    return gulp.src(assets.js)
        .pipe(gulp.dest(jsout));
});

gulp.task('copy-css-assets', function () {
    return gulp.src(assets.css)
        .pipe(gulp.dest(cssout));
});

var concatAndMinModule = function (module) {
    return gulp.src([module + '/static/**/*.js', '!**/*test*.js'])
        .pipe(concat(module + '.js'))
        .pipe(gulp.dest(jsout))
        .pipe(rename(module + '.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest(jsout));
};

gulp.task('concat-and-min', function () {
    concatAndMinModule('briefs');
    concatAndMinModule('quotes');
    concatAndMinModule('gallant');
    concatAndMinModule('calendr');
    concatAndMinModule('kanban');
    return;
});


gulp.task('concat-and-min-all', function () {
    return gulp.src(scripts)
        .pipe(concat('all.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest(jsout));
});

gulp.task('test', function (done) {
    new Server({
        configFile: __dirname + '/karma.conf.js',
    }, done()).start();
});

gulp.task('karma', function (done) {
    new Server({
        configFile: __dirname + '/karma.conf.js',
        singleRun: false,
        autoWatch: true,
    }, done()).start();
});

gulp.task('clean', function () {
    return del(['coverage', 'build']);
});

gulp.task('clean-coverage', function () {
    return del(['coverage']);
});

gulp.task('static', ['copy-js-assets', 'copy-css-assets', 'concat-and-min'])

gulp.task('production', ['copy-css-assets', 'copy-js-assets', 'concat-and-min-all'])

gulp.task('default', ['lint', 'copy-assets', 'test']);

gulp.task('watchStatic', function() {
    watch(scripts, function() {
        gulp.start('static');
    });
});
