app = angular.module('gallant.directives.glFormElements', [
]);

app.directive('glFormElements', [ function () {
    return {
        restrict: 'A',
        scope: {
            elements: '=',
            addFn: '=?',
            removeFn: '=?',
            language: '@',
        },
        controller: ['$scope', function ($scope) {
            $scope.addFn = function (e) { $scope.addElement(e); };
            $scope.removeFn = function (e) { $scope.removeElement(e); };
        }],
        templateUrl: function ($element, $attrs) {
            return $attrs.templateUrl ? $attrs.templateUrl : '';
        },
        link: function ($scope) {
            $scope.addElement = function () {
                if ($scope.language) {
                    $scope.elements.push({language: $scope.language});
                } else {
                    $scope.elements.push({});
                }
            };

            $scope.removeElement = function (index) {
                $scope.elements.splice(index, 1);
            };
        }
    };
}]);