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

        $scope.saveSettings = function() {
            $scope.user.$update({id: $scope.user.id});
        };

        $scope.$watchGroup(['openDashOnboarding', 'user.settings'], function (newVals, oldVals) {
            if ($scope.justLoggedIn && !$scope.opened &&
                    typeof(newVals[0]) == 'function' && typeof(newVals[1]) !== 'undefined') {
                if (!('hide_onboarding' in $scope.user.settings) || !$scope.user.settings.hide_onboarding) {
                    $scope.openDashOnboarding();
                    $scope.opened = true;
                }
            }
        });
    }
]);