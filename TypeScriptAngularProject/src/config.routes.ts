/// <reference path="_all.ts" />

module app.Configuration {
    'use strict';

    var app = angular.module('app');
    app.config([
        '$routeProvider',
        '$locationProvider', 
    ($routeProvider: ng.route.IRouteProvider, $locationProvider: ng.ILocationProvider) => {
            $routeProvider
                .when('/', {
                templateUrl: 'views/index.html'
            })
                .otherwise({
                redirectTo: '/'
            });
        }]);
}