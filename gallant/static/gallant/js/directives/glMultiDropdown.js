app = angular.module('gallant.directives.glMultiDropdown', [
]);

app.directive('glMultiDropdown', [ function () {
    return {
        restrict: 'A',
        scope: {
            elements: '=',
            availableElements: '=',
            elementDisplayName: '@',
        },
        controller: ['$scope', function ($scope) {
            /**
             * availableServices is an array containing available choices for each service select. When a service
             * is selected, it's removed from the other dropdowns via this function.
             */
            $scope.updateAvailableElements = function () {
                if ($scope.availableElements) {
                    if ($scope.elements.length) {
                        $scope.availableElementsSafe = [];
                        angular.forEach($scope.elements, function () {
                            $scope.availableElementsSafe.push($scope.availableElements.slice());
                        });
                        angular.forEach($scope.elements, function (s, si) {
                            angular.forEach($scope.availableElementsSafe, function (arr, i) {
                                if (i != si) {
                                    var idx = $scope.availableElementsSafe[i].findIndex(function (element) {
                                        return element.id == s;
                                    });
                                    if (idx >= 0)
                                        $scope.availableElementsSafe[i].splice(idx, 1);
                                }
                            });
                        });
                    } else {
                        $scope.availableElementsSafe = [$scope.availableElements.slice()];
                    }
                } else {
                    $scope.availableElementsSafe = [];
                }
            };

            $scope.$watch('availableElements', function () {
                $scope.updateAvailableElements();
            });

            $scope.$watch('elements', function () {
                $scope.updateAvailableElements();
            });
        }],
        templateUrl: '/static/gallant/html/gl_multi_dropdown.html',
        link: function ($scope) {
            $scope.addElement = function () {
                $scope.elements.push(-1);
                $scope.updateAvailableElements();
            };

            $scope.removeElement = function (index) {
                $scope.elements.splice(index, 1);
                $scope.updateAvailableElements();
            };
        }
    };
}]);