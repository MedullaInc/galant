app = angular.module('quotes.directives.qtClientForm', [
    'quotes.services.qtServices',
    'quotes.filters.qtCutFilter',
    'quotes.directives.qtServiceTable',
    'quotes.directives.qtSectionTable',
    'gallant.directives.glForm',
    'ui.bootstrap',
    'as.sortable']);

app.directive('qtClient', ['Quote', function (Quote) {
    return {
        restrict: 'A',
        scope: {
            quote: '=?',
            language: '=?',
            idType: '=?',
        },
        controller: ['$scope', '$attrs', '$filter', '$window', 'Quote',
            function ($scope, $attrs, $filter, $window, Quote) {
                var token = window.location.href.split('/').slice(-1).pop();
                $scope.idType = $attrs.idType;
                Quote.getUser({token: token}).$promise.then(function (quote) {
                    $scope.quote = quote;

                    if($attrs.idType == "token"){
                        $scope.quote.views  = $scope.quote.views+1;
                        if (parseInt($scope.quote.status) < 3) {
                            $scope.quote.status = "3";
                        }

                        Quote.updateUser({token: token}, $scope.quote);

                        $window.onbeforeunload  = function () {
                            Quote.updateUser({token: token}, {
                                views: $scope.quote.views,
                                session_duration: ((new Date() - $scope.$parent.startTime)/1000 ),
                                sections: $scope.quote.sections,
                                services: $scope.quote.services,
                            });
                        }
                    }

                });

                }],
        templateUrl: '/static/quotes/html/qt_quote_form.html',
        link: function ($scope) {}
    };
    }]);