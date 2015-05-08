var gulp = require('gulp');  
var ts = require('gulp-typescript');
var nodemon = require('gulp-nodemon');

var config = {
    tsFiles: ['src/**/*.ts'],
};

gulp.task('default', ['ts', 'watch']);

// Compile typescript sources
gulp.task('ts', function() {  
    gulp.src(config.tsFiles)
        .pipe(ts({
            module: 'commonjs',
            target: 'ES5'
         }))
        .js
        .pipe(gulp.dest('./wwwroot'));
});

gulp.task('watch', ['ts'], function() {  
    gulp.watch(config.tsFiles, ['ts']);
});

gulp.task('nodemon', ['watch'], function() {  
    nodemon({script: 'wwwroot/app.js'});
});