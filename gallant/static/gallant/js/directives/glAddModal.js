app = angular.module('gallant.directives.glAddModal', [
    'ui.bootstrap',
]);

app.directive("modalTransclude", function($parse){
  return {
    link: function($scope, $element, $attrs){
      $element.append($parse($attrs.modalTransclude)($scope));
    }
  };
});

app.directive('glAddModal', ['$uibModal', function ($uibModal) {
    return {
        restrict: 'A',
        replace: true,
        transclude: true,
        scope: {
            openFn: '=',
            objects: '=',
            title: '@',
        },
        controller: ['$scope', '$transclude', function ($scope, $transclude) {
            $scope.openFn = function() {
                $scope.modalInstance = $uibModal.open({
                    scope: $scope,
                    animation: true,
                    templateUrl: 'addModal.html',
                    controller: ['$scope', 'content', function ($scope, content) {
                        $scope.template = content;
                    }],
                    resolve: {
                        content: function () {
                            var transcludedContent;

                            $transclude(function (clone) {
                                transcludedContent = clone;
                            });

                            return transcludedContent;
                        },
                    },
                });
            };

            $scope.objectSaved = function (object) {
                $scope.objects.push(object);
                $scope.modalInstance.dismiss('cancel');
            };
        }],
        templateUrl: '/static/gallant/html/gl_add_modal.html',
        link: function ($scope) {
            $scope.cancel = function() {
                $scope.modalInstance.dismiss('cancel');
            }
        }
    };
}]);