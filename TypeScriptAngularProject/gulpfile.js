var gulp = require('gulp');  
var ts = require('gulp-typescript');
var concat = require("gulp-concat");
var uglify = require("gulp-uglify");
var minifyCSS = require('gulp-minify-css');
var clean = require('gulp-clean');

gulp.task('default', ['ts', 'watch']);

// Compile typescript sources
gulp.task('ts', function() {  
    gulp.src(['src/**/!(app)*.ts', 'src/app.ts'])
        .pipe(ts({module: 'commonjs', sortOutput: true}))
        .pipe(concat("app.min.js"))
        // .pipe(uglify())
        .pipe(gulp.dest('./wwwroot/js'));
});

// Minify and combine css into output folder
gulp.task('css', function() {
	gulp.src(['src/**/*.css'])
		.pipe(minifyCSS())
		.pipe(concat('style.min.css'))
		.pipe(gulp.dest('./wwwroot/css'));
});

// Concatenate all our external libraries to build folder
gulp.task('libraries', function() {
    gulp.src([
        'bower_components/jquery/dist/jquery.min.js',
        'bower_components/bootstrap/dist/js/bootstrap.min.js',
        'bower_components/angular/angular.min.js',
        'bower_components/angular-route/angular-route.min.js'
        ])
        .pipe(concat('libraries.min.js'))
        .pipe(gulp.dest('./wwwroot/js'));

    gulp.src([
        'bower_components/bootstrap/dist/css/bootstrap.css'
        ])
        .pipe(concat('libraries.min.css'))
        .pipe(gulp.dest('./wwwroot/css'));
});

gulp.task('watch', ['libraries', 'ts', 'css'], function() {  
    gulp.watch('./src/**/*.ts', ['ts']);
    gulp.watch('./src/**/*.css', ['css']);
});

// Remove built javascript and css from local folder
gulp.task('clean', function() {
    gulp.src(['wwwroot/js/**/*.js', 'wwwroot/css/**/*.css'])
        .pipe(clean());
});