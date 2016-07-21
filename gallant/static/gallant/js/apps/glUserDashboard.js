var app = angular.module('glUserDashboard', [
    'ngResource',
    'ui.bootstrap',
    'gallant.services.glServices',
    'gallant.directives.glDashboardWorkSummary',
    'gallant.directives.glDashboardMoneySummary',
    'gallant.controllers.glUserDashboardController',
    'gallant.directives.glAddModal',
    'tc.chartjs',
]);
