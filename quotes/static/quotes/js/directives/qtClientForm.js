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
            quote: '=',
            language: '=',
            idType: '=',
        },
        controller: ['$scope', '$attrs', '$filter', '$window', 'Quote',
            function ($scope, $attrs, $filter, $window, Quote) {
                $scope.idType = $attrs.idType;
                
                Quote.getUser({id: $attrs.quoteId, user: $attrs.userId}).$promise.then(function (quote) {
                    $scope.quote = quote;

                    if($attrs.idType == "token"){
                        $window.onload  = function () { 
                            var token = window.location.href.split('/').slice(-1).pop();
                            $scope.quote.session_duration = ((new Date() - $scope.$parent.startTime)/1000 );
                            $scope.quote.views  = $scope.quote.views+1;
                            $scope.quote.status = "3";
                            Quote.updateUser({id: $scope.quote.id, user: $attrs.userId}, $scope.quote);
                        }
                    }

                });

                }],
        templateUrl: '/static/quotes/html/qt_quote_form.html',
        link: function ($scope) {}
    };
    }]);