app = angular.module('gallant.controllers.glUserDashboardController', [
    'gallant.services.glServices',
    'gallant.directives.glAddModal',
]);

app.controller('glUserDashboardController', ['$scope', 'UserSettings',
    function ($scope, UserSettings) {
        $scope.user = {};
        $scope.opened = false;
        $scope.justLoggedIn = false;
        $scope.init = function(userId, justLoggedIn) {
            UserSettings.get({id: userId}).$promise.then(function (user) {
                $scope.user = user;
                $scope.justLoggedIn = justLoggedIn;
            });
        };

        $scope.$watchGroup(['openDashOnboarding', 'user.settings'], function (newVals, oldVals) {
            if ($scope.justLoggedIn && !$scope.opened &&
                    typeof(newVals[0]) == 'function' && typeof(newVals[1]) !== 'undefined') {
                $scope.openDashOnboarding();
                $scope.opened = true;
            }
        });
    }
]);