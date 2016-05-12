app = angular.module('quotes.directives.qtServiceTable', [
    'quotes.services.qtServices',
    ]);

app.directive('qtServiceTable', ['$window', 'Service', function ($window, Service) {
        return {
            restrict: 'A',
            scope: true,
            controller: ['$scope', '$filter', 'Service',

                function ($scope, $filter, Service) {
                    $scope.serviceFields = [];

                    if($scope.quote){
                        $filter('orderBy')($scope.quote.services, 'index');
                    }

                    Service.fields({}).$promise.then(function (fields) {
                        $scope.serviceFields = fields.type;
                    });

                }
            ],
            templateUrl: '/static/quotes/html/qt_quote_service_table.html',
            link: function ($scope) {

                $scope.removeService = function (index) {
                    if ($window.confirm('Remove service?')) {
                        $scope.quote.services.splice(index, 1);
                    }
                };

                $scope.getTotal = function () {
                    if ($scope.quote) {
                        if ($scope.quote.services) {
                            $scope.total = 0;
                            for (var i = 0; i < $scope.quote.services.length; i++) {
                                var service = $scope.quote.services[i];
                                if (service) {
                                    if(service.cost.amount > 0 && service.quantity > 0){
                                        $scope.total += (service.cost.amount * service.quantity);
                                    }else{
                                        $scope.total += 0;
                                    }
                                } else {
                                    $scope.total += 0;
                                }
                            }
                        }
                        return $scope.total;
                    }
                };

            }
        };
    }]);