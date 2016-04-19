describe('glForm', function () {
    var $rootScope;
    var $compile;
    var $scope;

    beforeEach(function () {
        module('gallant.directives.glForm');
        module('staticNgTemplates');

        inject(function (_$rootScope_, _$compile_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $compile = _$compile_;
        });


        $rootScope.language = 'en';
        $rootScope.text = {en: 'sadf'}
        $scope = $rootScope.$new();
    });

    describe('glRequiredErrors', function () {
        it('compiles', function () {
            var element = $compile('<div gl-required-errors></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 3)).toEqual('<ul');
        });
    });

    describe('glUltextInput', function () {
        it('compiles', function () {
            var element = $compile('<div gl-ultext-input></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 3)).toEqual('<in');
        });

        it('sets text', function () {
            var element = $compile('<div gl-ultext-input text="text" language="language"></div>')($scope);
            $scope.$digest();
            var inp = element.find('input');
            inp.val('hello').triggerHandler('input');
            expect($scope.text[$scope.language]).toEqual('hello');
        });
    });

    describe('glUltextArea', function () {
        it('compiles', function () {
            var element = $compile('<div gl-ultext-area></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 3)).toEqual('<te');
        });

        it('sets text', function () {
            var element = $compile('<div gl-ultext-area text="text" language="language"></div>')($scope);
            $scope.$digest();
            var inp = element.find('textarea');
            inp.val('hello').triggerHandler('input');
            expect($scope.text[$scope.language]).toEqual('hello');
        });
    });

    describe('glLanguageForm', function () {
        it('compiles', function () {
            var element = $compile('<div gl-language-form></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 3)).toEqual('<di');
        });
    });

    describe('glEditButtons', function () {
        it('compiles', function () {
            var element = $compile('<div gl-edit-buttons></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 3)).toEqual('<sp');
        });
    });
});

describe('glAlerts', function () {
    var $rootScope;
    var $compile;
    var $scope;

    beforeEach(function () {
        module('gallant.services.glServices', function ($provide) {
            $provide.factory('glAlertService', function () {
                return {
                    get: function () {
                        return {type: 'success', msg: '0'};
                    }
                };
            });
        });
        module('gallant.directives.glAlerts');

        inject(function (_$rootScope_, _$compile_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $compile = _$compile_;
        });

        $scope = $rootScope.$new();
    });

    describe('glAlerts', function () {
        it('compiles', function () {
            var element = $compile('<div gl-alerts></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 3)).toEqual('<!-');
        });
    });
});

describe('glPayments', function () {
    var $rootScope;
    var $compile;
    var $scope;

    beforeEach(function () {
        module('gallant.services.glServices', function ($provide) {

            $provide.factory('Payment', function ($q) {
                var Payment = {};
                Payment.delete = function (a) {
                    return {};
                };
                return Payment;
            });

            $provide.factory('$window', function () {
                return {
                    confirm: function (m) {
                        return true;
                    }
                };
            });

        });

        module('gallant.directives.glPayments');
        module('staticNgTemplates');

        inject(function (_$rootScope_, _$compile_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $compile = _$compile_;
        });

        $scope = $rootScope.$new();
    });

    describe('glPayments', function () {

        var element;

        beforeEach(function () {
            $scope.payments = [{id: 0}];
            element = $compile('<div gl-payments payments="payments"></div>')($scope);
            $scope.$digest();
        });

        it('compiles', function () {
            expect(element.html().substring(0, 3)).toEqual('<!-');
        });

        it('deletes a payment', function () {
            element.isolateScope().deletePayment($scope.payments[0]);
        });

    });

});

describe('glProjectList', function () {
    var $rootScope;
    var $compile;
    var $injector;
    var $scope;

    beforeEach(function () {
        angular.module('smart-table', []);

        module('gallant.services.glServices', function ($provide) {
            $provide.factory('Project', function ($q) {
                var Project = {};
                Project.query = function () {
                    return {$promise: $q.when([{}])};
                };
                return Project;
            });
        });

        module('gallant.directives.glProjectList', function ($provide) {
            $provide.value('$uibModal', {
                open: function () {
                    return {
                        dismiss: function () {
                        }
                    };
                }
            });
            $provide.value('$window', {location: {}});
        });
        module('staticNgTemplates');

        inject(function (_$rootScope_, _$compile_, _$injector_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $compile = _$compile_;
            $injector = _$injector_;
        });

        $scope = $rootScope.$new();
    });

    describe('glProjectList', function () {

        var element;

        beforeEach(function () {
            element = $compile('<div gl-project-list=""></div>')($scope);
            $scope.$digest();
        });

        it('compiles', function () {
            expect(element.html().substring(0, 6)).toEqual('<scrip');
        });

        it('adds project', function () {
            var $uibModal = $injector.get('$uibModal');
            spyOn($uibModal, 'open');
            element.isolateScope().addProject();
            $scope.$apply();
            expect($uibModal.open).toHaveBeenCalled();
        });

        it('saves project', function () {
            element.isolateScope().addProject();
            spyOn(element.isolateScope().modalInstance, 'dismiss');
            element.isolateScope().projectSaved({});
            $scope.$apply();
            expect(element.isolateScope().projectsSafe.length).toEqual(2);
            expect(element.isolateScope().modalInstance.dismiss).toHaveBeenCalled();
        });

        it('cancels', function () {
            element.isolateScope().addProject();
            spyOn(element.isolateScope().modalInstance, 'dismiss');
            element.isolateScope().cancel();
            $scope.$apply();
            expect(element.isolateScope().modalInstance.dismiss).toHaveBeenCalled();
        });

        it('redirects', function () {
            var $window = $injector.get('$window');
            element.isolateScope().redirect({link: ''});
            expect($window.location.href).toBeDefined();
        });

        it('selects projects', function () {
            element.isolateScope().selectedAll = true;
            element.isolateScope().checkAll();
            expect(element.isolateScope().projectsSafe[0].isSelected).toEqual(true);
        });
    });
});

describe('glProjectAdd', function () {
    var $rootScope;
    var $compile;
    var $scope;

    beforeEach(function () {
        module('gallant.services.glServices', function ($provide) {
            $provide.factory('Project', function ($q) {
                var Project = function () {
                };
                Project.fields = function () {
                    return {$promise: $q.when([])};
                };
                return Project;
            });

            $provide.factory('Quote', function ($q) {
                var Quote = function () {
                };
                Quote.query = function () {
                    return {$promise: $q.when([])};
                };
                return Quote;
            });
        });

        module('gallant.directives.glProjectAdd');

        module('staticNgTemplates');

        inject(function (_$rootScope_, _$compile_, _$injector_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $compile = _$compile_;
        });

        $scope = $rootScope.$new();
    });

    describe('glProjectAdd', function () {

        var element;

        beforeEach(function () {
            element = $compile('<div gl-project-add="" project="project" endpoint="endpoint"></div>')($scope);
            $scope.$digest();
        });

        it('compiles', function () {
            expect(element.html().substring(0, 6)).toEqual('<div c');
        });
    });
});

describe('glClientMoneyChart', function () {
    var $rootScope;
    var $compile;
    var $scope;

    beforeEach(function () {
        angular.mock.module('gallant.services.glServices', function ($provide) {
            $provide.factory('Payment', function ($q) {
                var Payment = jasmine.createSpyObj('Payment', ['query']);
                Payment.query.and.returnValue({
                    $promise: $q.when([{
                        paid_on: new Date(),
                        amount: {amount: 1.0}
                    }, {paid_on: null, due: new Date() + 10, amount: {amount: 1.0}}, {
                        paid_on: null,
                        due: new Date() - 10,
                        amount: {amount: 1.0}
                    }])
                });

                return Payment;
            });
        });

        angular.mock.module('gallant.directives.glClientMoneyChart');
        angular.mock.module('staticNgTemplates');
        angular.module('tc.chartjs', []);

        angular.mock.inject(function (_$rootScope_, _$compile_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $compile = _$compile_;
        });

        $scope = $rootScope.$new();
    });

    describe('glClientMoneyChart', function () {

        var element;

        beforeEach(function () {
            element = $compile('<span gl-client-money-chart=""></span>')($scope);
            $scope.$digest();
        });

        it('compiles', function () {
            expect(element.html().substring(0, 6)).toEqual('<div c');
        });
    });
});

describe('glClientWorkChart', function () {
    var $rootScope;
    var $compile;
    var $scope;

    beforeEach(function () {
        angular.mock.module('gallant.services.glServices', function ($provide) {
            $provide.factory('Service', function ($q) {
                var Service = jasmine.createSpyObj('Service', ['query']);
                Service.query.and.returnValue({$promise: $q.when([{status: 0}, {status: 1}, {status: 2}, {status: 3}, {status: 4}])});

                return Service;
            });
        });

        angular.mock.module('gallant.directives.glClientWorkChart');
        angular.mock.module('staticNgTemplates');
        angular.module('tc.chartjs', []);

        angular.mock.inject(function (_$rootScope_, _$compile_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $compile = _$compile_;
        });

        $scope = $rootScope.$new();
    });

    describe('glClientWorkChart', function () {

        var element;

        beforeEach(function () {
            element = $compile('<span gl-client-work-chart=""></span>')($scope);
            $scope.$digest();
        });

        it('compiles', function () {
            expect(element.html().substring(0, 6)).toEqual('<div c');
        });
    });
});

describe('glMultiDropdown', function () {
    var $rootScope;
    var $compile;
    var $scope;

    beforeEach(function () {
        module('gallant.directives.glMultiDropdown');
        module('staticNgTemplates');

        inject(function (_$rootScope_, _$compile_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $compile = _$compile_;
        });

        $scope = $rootScope.$new();
    });

    describe('glMultiDropdown', function () {

        var element;
        it('compiles', function () {
            element = $compile('<span gl-multi-dropdown=""></span>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 6)).toEqual('<div c');
        });

        it('adds element', function () {
            $scope.elements = [];
            $scope.availableElements = [{id: 0}, {}];
            element = $compile('<span gl-multi-dropdown="" elements="elements" ' +
                'available-elements="availableElements"></span>')($scope);
            $scope.$digest();
            element.isolateScope().addElement();
            expect(element.isolateScope().elements.length).toEqual(1);
        });

        it('removes element', function () {
            $scope.elements = [0, -1];
            $scope.availableElements = [{}, {id: 0}];
            element = $compile('<span gl-multi-dropdown="" elements="elements" ' +
                'available-elements="availableElements"></span>')($scope);
            $scope.$digest();
            element.isolateScope().removeElement(0);
            expect(element.isolateScope().elements.length).toEqual(1);
        });
    });

});

describe('glDashboardWorkSummary', function () {
    var $rootScope;
    var $compile;
    var $scope;

    beforeEach(function () {

        angular.mock.module('gallant.directives.glDashboardWorkSummary');
        angular.mock.module('staticNgTemplates');
        angular.module('tc.chartjs', []);

        angular.mock.inject(function (_$rootScope_, _$compile_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $compile = _$compile_;
        });

        $scope = $rootScope.$new();
    });

    describe('glDashboardWorkSummary', function () {

        var element;

        beforeEach(function () {
            element = $compile('<div gl-dashboard-work-summary=""></div>')($scope);
            $scope.$digest();
        });

        it('compiles', function () {
            expect(element.html().substring(0, 6)).toEqual('<div c');
        });
    });
});

describe('glDashboardMoneySummary', function () {
    var $rootScope;
    var $compile;
    var $scope;

    beforeEach(function () {

        angular.mock.module('gallant.directives.glDashboardMoneySummary');
        angular.mock.module('staticNgTemplates');
        angular.module('tc.chartjs', []);

        angular.mock.inject(function (_$rootScope_, _$compile_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $compile = _$compile_;
        });

        $scope = $rootScope.$new();
    });

    describe('glDashboardMoneySummary', function () {

        var element;

        beforeEach(function () {
            element = $compile('<div gl-dashboard-money-summary=""></div>')($scope);
            $scope.$digest();
        });

        it('compiles', function () {
            expect(element.html().substring(0, 6)).toEqual('<div c');
        });
    });
});
