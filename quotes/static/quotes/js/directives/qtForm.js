app = angular.module('quotes.directives.qtForm', [
    'gallant.directives.glForm',
    'quotes.services.qtServices',
    'quotes.filters.qtCutFilter',
    'quotes.directives.qtServiceTable',
    'quotes.directives.qtSectionTable',
    'gallant.services.glServices',
    'ui.bootstrap',
    'as.sortable']);

app.directive('qtQuoteForm', ['Quote', '$uibModal', function (Quote, $uibModal) {
    return {
        restrict: 'A',
        scope: {
            quote: '=?',
            quoteTemplate: '=?',
            endpoint: '=?',
            language: '=?',
            forms: '=?',
            boolTemplate: '=?',
            idType: '=?',
            deleteObject: '&',
            submit: '&',
        },
        controller: ['$scope', '$attrs', '$filter', '$window', 'Quote', 'Service', 'Section', 'QuoteTemplate', 'Client', 'LANGUAGES', 'glValidate',
            function ($scope, $attrs, $filter, $window, Quote, Service, Section, QuoteTemplate, Client, LANGUAGES, glValidate) {
                $scope.quoteFields = [];
                $scope.serviceFields = [];
                $scope.quoteStatus = {};
                $scope.quoteLanguage = {};
                $scope.newQuote = false;
                $scope.sortDisabled = false;
                $scope.tempStatus = '0';
                $scope.validate = glValidate;
                $scope.submitForm = $scope.submit();

                $scope.idType = $attrs.idType;
                $scope.boolTemplate = $attrs.boolTemplate;

                Client.query().$promise.then(function (clients) {
                    $scope.clients = clients;
                });

                Service.get().$promise.then(function (services) {
                    $scope.services = services;
                });


                Service.fields({}).$promise.then(function (fields) {
                    $scope.serviceFields = fields.type;
                });

                Quote.fields().$promise.then(function (fields) {
                    $scope.quoteStatus = fields.status;
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
                    $scope.section = new Section({"name": name, "index": counter, "views": 0});
                    $scope.section.index = counter++;
                    delete $scope.section.id;
                    if ($scope.quoteform && !$scope.quoteform.$visible) {
                        $scope.quoteform.$show();
                    }
                    $scope.quote.sections.push($scope.section);
                };

                $scope.addService = function (service) {
                    var counter = $scope.quote.services.length;

                    if (service) {
                        $scope.service = service;
                        $scope.modalInstance.close();
                    } else {
                        $scope.service = new Service();
                        $scope.service.description = {}
                        $scope.service.user = $scope.quote.user;
                        $scope.service.cost = {amount: 0, currency: "USD"}
                    }
                    $scope.service.user = $scope.quote.user;
                    $scope.service.index = counter++;
                    delete $scope.service.id;
                    if ($scope.quoteform && !$scope.quoteform.$visible) {
                        $scope.quoteform.$show();
                    }
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
                        $scope.quote.services = $filter('orderBy')($scope.quote.services, 'index');
                        $scope.quote.sections = $filter('orderBy')($scope.quote.sections, 'index');

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

                            var lang = LANGUAGES.find(function (x) { return x.code == $scope.language;});
                            $scope.quoteTemplate.languages = [lang];
                            if ($scope.quoteform.$show) {
                                $scope.quoteform.$show();
                            }

                        }

                    });
                } else if ($attrs.templateId) {
                    QuoteTemplate.get({
                        id: $attrs.templateId
                    }).$promise.then(function (quoteTemplate) {
                        $scope.quoteTemplate = quoteTemplate;
                        $scope.quote = quoteTemplate.quote;
                        $scope.quote.services = $filter('orderBy')($scope.quote.services, 'index');
                        $scope.quote.sections = $filter('orderBy')($scope.quote.sections, 'index');
                        $scope.tempStatus = $scope.quote.status;
                        if ($attrs.boolTemplate != "True") {
                            delete $scope.quote.id;

                            angular.forEach($scope.quote.sections, function (q) {
                                delete q.id;
                            });
                            angular.forEach($scope.quote.services, function (q) {
                                delete q.id;
                            });

                            if ($scope.quoteform.$show) {
                                $scope.quoteform.$show();
                            }
                        }

                        if ($scope.quoteTemplate.languages.length == 0) {
                            var lang = LANGUAGES.find(function (x) { return x.code == $scope.language;});
                            $scope.quoteTemplate.languages = [lang];
                        }

                        $scope.quote.language = $scope.language;
                    });
                } else {
                    $scope.quote = new Quote();
                    $scope.quote.user = $attrs.userId;
                    $scope.quote.client = $attrs.clientId;
                    $scope.quote.projects = [];
                    $scope.quote.services = [];
                    $scope.quote.sections = [];
                    $scope.quote.language = $scope.language;
                    $scope.quote.status = 0;
                    $scope.quote.views = 0;
                    $scope.quote.session_duration = 0.0;

                    $scope.quoteTemplate = {"quote": $scope.quote};
                    $scope.quoteTemplate.languages = [];

                    if ($scope.language && LANGUAGES.length > 0) {
                        var lang = LANGUAGES.find(function (x) { return x.code == $scope.language;});
                        $scope.quoteTemplate.languages = [lang];
                    }

                    $scope.addSection('intro');
                    $scope.addSection('important_notes');
                    $scope.addService();
                    $scope.newQuote = true;
                    $scope.tempStatus = $scope.quote.status;
                }
                $scope.dragControlListeners = {
                    accept: function (sourceItemHandleScope, destSortableScope) {
                        return sourceItemHandleScope.itemScope.sortableScope.$id === destSortableScope.$id;
                    }
                };


                $scope.storeQuote = function () {
                    $scope.storedQuote = JSON.stringify($scope.quote);
                };

                $scope.loadStoredQuote = function () {
                    $scope.quote = JSON.parse($scope.storedQuote);
                };
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

            var submitWithoutOnAfterSave = function(form) {
                var tmpFn = form.$onaftersave;
                form.$onaftersave = angular.noop;
                form.$submit();
                form.$onaftersave = tmpFn;
            };

            $scope.setLanguage = function (language) {
                var initVis = $scope.quoteform.$visible;
                if (initVis) {
                    submitWithoutOnAfterSave($scope.quoteform);
                }
                if (!$scope.quoteform.$visible) {
                    $scope.language = language;
                    if (initVis)
                        $scope.quoteform.$show();
                }
            };

            $scope.addLanguage = function (language) {
                if ($scope.quoteform.$visible) {
                    submitWithoutOnAfterSave($scope.quoteform);
                }

                if (!$scope.quoteform.$visible) {
                    $scope.quoteTemplate.languages.push(language);
                    $scope.setLanguage(language.code);
                    $scope.quoteform.$show();
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

            $scope.showType = function (service) {
                if (service) {
                    return $scope.serviceFields[service.type];
                }
            };

            /* show functions depending on status */
            $scope.showViews = function () {
                if ($scope.tempStatus == '3' && $scope.idType != 'token') {
                    return true;
                }
            };

            $scope.showEdit = function () {
                if (( $scope.tempStatus == '0' || $scope.tempStatus == '1' )
                    && $scope.idType != 'token') {
                    return true;
                }
            };

            $scope.hideCancel = function () {
                if (($scope.quote && !$scope.quote.name) ||
                    ($scope.boolTemplate == "False" && $scope.quote && !$scope.quote.client)) {
                    return true;
                }
            };

            $scope.showClient = function () {
                if ($scope.boolTemplate != 'True' && $scope.idType != 'token') {
                    return true;
                }
            };
        }
    };
}]);