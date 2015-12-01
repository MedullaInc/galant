// Include gulp
var gulp = require('gulp');

// Include Our Plugins
var jshint = require('gulp-jshint');

var scripts = ['**/static/**/*.js',
    '!static/**', '!venv/**', '!node_modules/**']

// Lint Task
gulp.task('lint', function() {
    return gulp.src(scripts)
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
});

gulp.task('default', ['lint']);
