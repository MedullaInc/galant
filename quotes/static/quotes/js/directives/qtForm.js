app = angular.module('quotes.directives.qtForm', [
    'quotes.services.qtServices',
    'quotes.filters.qtCutFilter',
    'quotes.directives.qtServiceTable',
    'quotes.directives.qtSectionTable',
    'gallant.directives.glForm',
    'ui.bootstrap',
    'as.sortable']);

app.directive('qtQuoteForm', ['Quote', 'Service', 'Section', 'Client', '$filter', '$uibModal', function (Quote, Service, Section, Client, $filter, $uibModal) {
    return {
        restrict: 'A',
        scope: {
            quote: '=',
            quoteTemplate: '=',
            endpoint: '=',
            language: '=',
            forms: '=',
            boolTemplate: '=',
            idType: '=',
        },
        controller: ['$scope', '$attrs', '$filter', '$window', 'Quote', 'Service', 'Section', 'QuoteTemplate', 'Client',
            function ($scope, $attrs, $filter, $window, Quote, Service, Section, QuoteTemplate, Client) {
                $scope.quoteFields   = [];
                $scope.quoteStatus   = {};
                $scope.quoteLanguage = {};
                $scope.newQuote      = false;
                $scope.tempStatus    = '0';

                $scope.idType = $attrs.idType;
                $scope.boolTemplate = $attrs.boolTemplate;

                if($attrs.idType == "token"){
                    $window.onbeforeunload  = function () { 
                        $scope.quote.session_duration = ((new Date() - $scope.$parent.startTime)/1000 );
                        $scope.quote.views  = $scope.quote.views+1;
                        $scope.quote.status = "3";
                        Quote.update({id: $scope.quote.id}, $scope.quote);
                    }
                }

                Client.get().$promise.then(function (clients) {
                    $scope.clients = clients;
                });

                Quote.fields().$promise.then(function (fields) {
                    $scope.quoteStatus   = fields.status;
                    $scope.quoteLanguage = fields.language;
                });

            $scope.addSection = function (section_name) {
                var counter = $scope.quote.sections.length;
                var name = "";

                if (section_name) {
                    name = section_name;
                } else {    
                    name = "section_" + (counter++);
                }
                $scope.section              = new Section({"name":name, "index":counter, "text":{}, "title":{}, "views":0});
                $scope.section.index        = counter++;
                delete $scope.section.id;
                $scope.quote.sections.push($scope.section);
            };

            $scope.addService = function (service) {
                var counter = $scope.quote.services.length;

                if (service) {
                    $scope.service = service;
                    $scope.modalInstance.close();
                } else {
                    $scope.service              = new Service();
                    $scope.service.name         = {}
                    $scope.service.description  = {}
                    $scope.service.user         = $scope.quote.user;
                    $scope.service.cost         = {amount:0, currency:"USD"}
                }
                $scope.service.user         = $scope.quote.user;
                $scope.service.index        = counter++;
                delete $scope.service.id;
                $scope.quote.services.push($scope.service);
            };
                

                if ($attrs.boolTemplate == "False") {
                    $scope.endpoint = Quote;
                } else {
                    $scope.endpoint = QuoteTemplate;
                }

                if ($attrs.quoteId) {
                    Quote.get({id: $attrs.quoteId, user: $attrs.userId}).$promise.then(function (quote) {
                        $scope.quote = quote;
                        $scope.tempStatus = $scope.quote.status;

                        if ($attrs.boolTemplate == "True") {
                            $scope.quoteTemplate = {
                                "quote": $scope.quote
                            };

                            delete $scope.quoteTemplate.quote.id;
                            angular.forEach($scope.quote.sections, function (q) {
                                delete q.id;
                            });
                            angular.forEach($scope.quote.services, function (q) {
                                delete q.id;
                            });

                            $scope.quoteTemplate.languages  = [];
                        }

                    });
                } else if ($attrs.templateId) {
                        QuoteTemplate.get({
                            id: $attrs.templateId
                        }).$promise.then(function (quoteTemplate) {
                            $scope.quoteTemplate = quoteTemplate;
                            $scope.quote = quoteTemplate.quote;
                            $scope.tempStatus = $scope.quote.status;
                            if ($attrs.boolTemplate != "True") {
                                delete $scope.quote.id;
                            }

                            angular.forEach($scope.quote.sections, function (q) {
                                delete q.id;
                            });
                            angular.forEach($scope.quote.services, function (q) {
                                delete q.id;
                            });

                        });
                    } else {
                        $scope.quote                    = new Quote();
                        $scope.quote.user               = $attrs.userId;
                        $scope.quote.client             = $attrs.clientId;
                        $scope.quote.projects           = [];
                        $scope.quote.services           = [];
                        $scope.quote.sections           = [];
                        $scope.quote.status             = 0;
                        $scope.quote.views              = 0;
                        $scope.quote.session_duration   = 0.0;

                        $scope.quoteTemplate            = {"quote": $scope.quote};
                        $scope.quoteTemplate.languages  = [];

                        $scope.addSection('intro');
                        $scope.addSection('important_notes');
                        $scope.addService();
                        $scope.newQuote                 = true;
                        $scope.tempStatus               = $scope.quote.status;
                    }
                }],
        templateUrl: '/static/quotes/html/qt_quote_form.html',
        link: function ($scope) {
            
            /*  TODO validate selected client onbeforesave
            if($scope.newQuote){
                //$scope.quoteform.$show();
            }

            $scope.checkClient = function (data){
                if (!data) {
                  return "Plase select a client";
                }
            }
            */

            $scope.dynamicPopover = {
                translationTemplateUrl: 'translationTemplate.html',
                serviceTemplateUrl: 'serviceTemplate.html'
            };

            $scope.changeLanguage = function (lang) {
                $scope.language = lang;
            };

            $scope.setLanguage = function (language) {
                $scope.language = language;
            };

            $scope.addLanguage = function (language) {
                $scope.quoteTemplate.languages.push(language);
            };

            $scope.showRowForm = function (rowform) {
                if ($scope.quote.status != '2') {
                    rowform.$show();
                }
            };

            $scope.open = function () {
                $scope.modalInstance = $uibModal.open({
                    scope: $scope,
                    animation: true,
                    templateUrl: 'myModalContent.html'
                });
                return 0;
            };

            /* show functions depending on status */
            $scope.showViews = function () {
                if ($scope.tempStatus == '3' && $scope.idType != 'token'){
                    return true;
                }
            }

            $scope.showEdit = function() {
                if (( $scope.tempStatus == '0' || $scope.tempStatus == '1' )
                    && $scope.idType != 'token'){
                    return true;
                }
            };

            $scope.showClient = function() {
                if ($scope.boolTemplate != 'True' && $scope.idType != 'token' ){
                    return true;
                }
            };

        }
    };
    }]);