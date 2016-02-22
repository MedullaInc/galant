app = angular.module('quotes.directives.qtServiceTable', [
    'quotes.services.qtServices',
    ]);

app.directive('qtServiceTable', ['Service', function (Service) {
        return {
            restrict: 'A',
            scope: true,
            controller: ['$scope', 'Service',
                function ($scope, Service) {
                    $scope.serviceFields = [];
                    Service.fields({}).$promise.then(function (fields) {
                        $scope.serviceFields = fields.type;
                    });

                }
            ],
            templateUrl: '/static/quotes/html/qt_quote_service_table.html',
            link: function ($scope) {

                $scope.showService = function (service){
                    if($scope.idType == "token"){
                        id = service.id;
                        service.views = service.views+1;
                        Service.update({id: id, user: $scope.quote.user}, service);
                    }
                }

                $scope.removeService = function (index) {
                    $scope.quote.services.splice(index, 1);
                };

                $scope.getTotal = function () {
                    if ($scope.quote) {
                        if ($scope.quote.services) {
                            $scope.total = 0;
                            for (var i = 0; i < $scope.quote.services.length; i++) {
                                var service = $scope.quote.services[i];
                                if (service) {
                                    $scope.total += (service.cost.amount * service.quantity);
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