app = angular.module('quotes.controllers.qtQuoteListController', ['quotes.services.qtServices','ngAnimate']);

app.controller('qtQuoteListController', ['$scope', '$http', '$window', 'Quote', 'QuoteTemplate', 'Client',
    function($scope, $http, $window, Quote, QuoteTemplate, Client) {
        $scope.quotes = [];
        $scope.quoteStatus = [];
        $scope.clients = [];

        $scope.init = function(quoteDetailURL, currentLanguage) {
            $scope.quoteDetailURL = quoteDetailURL;
            $scope.currentLanguage = currentLanguage;
        };

        Quote.fields().$promise.then(function(fields) {
            for (var key in fields.status) {
                // must create a temp object to set the key using a variable
                var tempObj = {};
                tempObj[key] = fields.status[key];
                $scope.quoteStatus.push({
                    value: key,
                    text: tempObj[key]
                });
            }
        });

        Quote.query().$promise.then(function(quotes) {
            $scope.quotesSafe = quotes;
        });

        QuoteTemplate.query().$promise.then(function(quoteTemplates) {
            $scope.quoteTemplates = quoteTemplates;
        });    

        Client.query().$promise.then(function(clients) {
            $scope.clients = clients;
        });

        $scope.redirect = function(id) {
            $window.location.href = $scope.quoteDetailURL + id
        };

    }

])

app.filter('myStrictFilter', function($filter){
    return function(input, predicate){
        return $filter('filter')(input, predicate, true);
    }
});

app.filter('unique', function() {
    return function (arr, field) {
        var o = {}, i, l = arr.length, r = [];
        for(i=0; i<l;i+=1) {
            o[arr[i][field]] = arr[i];
        }
        for(i in o) {
            r.push(o[i]);
        }
        return r;
    };
  });