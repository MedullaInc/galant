app = angular.module('quotes.directives.qtForm', [
    'quotes.services.qtServices',
    'quotes.filters.qtCutFilter',
    'quotes.directives.qtServiceTable',
    'quotes.directives.qtSectionTable',
    'gallant.directives.glForm',
    'ui.bootstrap',
    'as.sortable']);

app.directive('qtQuoteForm', ['Quote', 'Service','Section', 'Client', '$filter', '$uibModal', function (Quote, Service, Section, Client, $filter, $uibModal) {
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
                    $scope.quoteFields = [];
                    $scope.quoteStatus = {};
                    $scope.quoteLanguage = {};
                    $scope.language_list = {};

                    $scope.idType = $attrs.idType;
                    $scope.boolTemplate = $attrs.boolTemplate;

                    if($attrs.idType == "token"){
                        $window.onbeforeunload = function () { 
                            $scope.quote.session_duration = ((new Date() - $scope.$parent.startTime)/1000 );
                            $scope.quote.views = $scope.quote.views+1;
                            $scope.quote.status = "3";
                            Quote.update({id: $scope.quote.id}, $scope.quote);
                        }
                    }

                    Client.get().$promise.then(function (clients) {
                        $scope.clients = clients;
                    });

                    Quote.fields().$promise.then(function (fields) {
                        $scope.quoteStatus = fields.status;
                        $scope.quoteLanguage = fields.language;
                    });

                $scope.addSection = function (section_name) {
                    var name = "";
                    var counter;

                    if (section_name) {
                        name = section_name;
                    } else {
                        counter = $scope.quote.sections.length;
                        name = "section_" + (counter++);
                    }

                    $scope.inserted = {
                        title: {},
                        text: {},
                        name: name,
                        index: counter,
                        views: 0,
                    };
                    $scope.quote.sections.push($scope.inserted);
                };

                $scope.addService = function (service) {
                    if (service) {
                        $scope.insertedService = service;
                        $scope.modalInstance.close();
                    } else {
                        $scope.insertedService = {
                            cost: {
                                amount: "0",
                                currency: "USD"
                            },
                            user: $scope.quote.user,
                            name: "",
                            description: "",
                            notes: Array[0],
                            parent: null,
                            quantity: "",
                            type: "",
                            views: 0,
                        };
                    }
                    $scope.quote.services.push($scope.insertedService);
                };
                    

                    if ($attrs.boolTemplate == "False") {
                        $scope.endpoint = Quote;
                    } else {
                        $scope.endpoint = QuoteTemplate;
                    }

                    if ($attrs.quoteId) {
                        Quote.get({id: $attrs.quoteId}).$promise.then(function (quote) {
                            $scope.quote = quote;
                            if ($scope.language) {
                                $scope.language_list[$scope.language] = $scope.quoteLanguage[$scope.language];
                            }

                            if ($attrs.boolTemplate == "True") {
                                $scope.quoteTemplate = {
                                    "quote": $scope.quote
                                };
                                $scope.quoteTemplate.quote.id = null;
                            }

                        });
                    } else {
                        if ($attrs.templateId) {
                            QuoteTemplate.get({
                                id: $attrs.templateId
                            }).$promise.then(function (quoteTemplate) {
                                $scope.quote = quoteTemplate.quote;
                                $scope.quoteTemplate = quoteTemplate;
                                $scope.language_list = quoteTemplate.language_list;

                                if ($attrs.boolTemplate != "True") {
                                    $scope.quote.id = null;
                                }

                            });
                        } else {
                            $scope.quote = {
                                "id": null,
                                "user": $attrs.userId,
                                "name": "New Quote",
                                "client": $attrs.clientId,
                                "sections": [],
                                "services": [],
                                "status": "0",
                                "modified": "",
                                "token": "",
                                "parent": null,
                                "projects": [],
                                "views": 0,
                                "session_duration": 0.0,
                            };

                            $scope.quoteTemplate = {
                                "quote": $scope.quote
                            };

                            $scope.addSection('intro');
                            $scope.addSection('important_notes');
                            $scope.addService();
                        }

                    }
                }
            ],
            templateUrl: '/static/quotes/html/qt_quote_form.html',
            link: function ($scope) {

                $scope.dynamicPopover = {
                    translationTemplateUrl: 'translationTemplate.html',
                    serviceTemplateUrl: 'serviceTemplate.html'
                };

                $scope.changeLanguage = function (lang) {
                    $scope.language = lang;
                };

                $scope.addLanguage = function (lang) {
                    $scope.language_list[lang] = $scope.quoteLanguage[lang];
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

            }
        };
    }]);