describe('glClientListController', function () {
    var $rootScope;
    var $controller;
    var $window;
    var url = 'about:blank';

    beforeEach(function () {
        angular.module('gallant.services.glServices', []);
        module('gallant.services.glServices', function ($provide) {
            $provide.factory('Client', function ($q) {
                var Client = jasmine.createSpyObj('Client', ['query', 'fields', 'update']);

                Client.query.and.returnValue({$promise: $q.when([{id: 0, last_contacted: null}])});
                Client.fields.and.returnValue({$promise: $q.when({})});
                Client.update.and.returnValue({$promise: $q.when({})});

                return Client;
            });
            $provide.factory('glConstants', function() {
                return {};
            });
        });
        module('gallant.controllers.glClientListController', function ($provide) {
            $provide.value('$window', {location: {href: null}});
        });

        inject(function (_$rootScope_, _$controller_, _$window_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $controller = _$controller_;
            $window = _$window_;
        });
    });

    var $scope;

    beforeEach(function () {
        $scope = $rootScope.$new();
        $controller('glClientListController', {$scope: $scope});
        $scope.init(url);
        $rootScope.$apply();
        $scope.clients = $scope.clientsSafe;
    });

    it('sets clientDetailURL', function () {
        expect($scope.clientDetailURL).toEqual(url);
    });

    it('generates clientDetail redirect URL', function () {
        $scope.redirect({id: 4});
        expect($window.location.href).toEqual(url + '4');
    });

    it('gets client list', function () {
        expect($scope.clients.length).toEqual(1);
    });

    it('updates client last_modified', function () {
        expect($scope.clients[0].last_contacted).toBeNull();
        $scope.updateLastContacted(0);
        $rootScope.$apply();
        expect($scope.clients[0].last_contacted).not.toBeNull();
    });

    it('saves client', function () {
        $scope.modalInstance = { dismiss: function () {} };
        $scope.clientSaved({});
        expect($scope.clients.length).toEqual(2);
    });
});

describe('glProjectDetailController', function () {
    var $rootScope;
    var $controller;
    var $window;
    var url = 'about:blank';

    beforeEach(function () {
        angular.module('gallant.services.glServices', []);
        module('gallant.services.glServices', function ($provide) {
            $provide.factory('Project', function ($q) {
                return {
                    get: function () {
                        return {
                            $promise: $q.when({
                                id: 0, services: [{id: 0, name: {}, description: {}, language: 'en'}]
                            })
                        };
                    },
                    update: function (id, project) {
                        return {
                            $promise: $q.when(project)
                        };
                    }
                };
            });
            $provide.factory('glConstants', function() {
                return {};
            });
        });
        module('gallant.controllers.glProjectDetailController', function ($provide) {
            $provide.value('$window', {location: {href: null, reload: function () {} }});
        });

        inject(function (_$rootScope_, _$controller_, _$window_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $controller = _$controller_;
            $window = _$window_;
        });
    });

    var $scope;

    beforeEach(function () {
        $scope = $rootScope.$new();
        $controller('glProjectDetailController', {$scope: $scope});
        $scope.init(url, 1);
        $rootScope.$apply();
    });

    it('sets serviceDetailURL', function () {
        expect($scope.serviceDetailURL).toEqual(url);
    });

    it('generates serviceDetail redirect URL', function () {
        $scope.redirect({id: 4});
        expect($window.location.href).toEqual(url + '4');
    });

    it('gets service list', function () {
        expect($scope.services.length).toEqual(1);
    });

    it('creates a copy on edit', function () {
        $scope.editProject = jasmine.createSpy('editProject');
        $scope.editProjectSafe();
        $scope.$apply();

        expect($scope.projectSafe).toBeDefined();
        expect($scope.editProject).toHaveBeenCalled();
    });

    it('saves project', function () {
        spyOn($window.location, 'reload');
        $scope.modalInstance = { dismiss: function () {} };
        $scope.projectSaved({});
        expect($window.location.reload).toHaveBeenCalled();
    });

    it('saves deliverable', function () {
        $scope.modalInstance = { dismiss: function () {} };
        spyOn($scope.modalInstance, 'dismiss');
        $scope.saveDeliverable({});
        $scope.$apply();
        expect($scope.modalInstance.dismiss).toHaveBeenCalled();
    });
});

describe('glFormController', function () {
    var $rootScope;
    var $controller;
    var window;

    beforeEach(function () {
        module('gallant.controllers.glFormController', function ($provide) {
            $provide.factory('glAlertService', function ($q) {
                return {};
            });
        });

        inject(function (_$rootScope_, _$controller_, _$window_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $controller = _$controller_;
            $window = _$window_;
        });
    });

    var $scope;
    var lang = 'es';
    var url = 'http://foo.com/';

    beforeEach(function () {
        $scope = $rootScope.$new();
        $controller('glFormController', {$scope: $scope});
        $scope.init(lang, 'csrftoken');
        $rootScope.$apply();
        $scope.object = {};

        $scope.objectEndpoint = {};
        $scope.objectEndpoint.save = function (a, b, callback) {
            callback({redirect: url});
        };
        $scope.objectEndpoint.update = function (a, b, callback) {
            callback({redirect: url});
        };
        $scope.objectEndpoint.delete = function (a, callback) {
            callback({redirect: url});
        };

        spyOn($scope.objectEndpoint, 'save').and.callThrough();
        spyOn($scope.objectEndpoint, 'update').and.callThrough();
        spyOn($scope.objectEndpoint, 'delete').and.callThrough();

        $scope.forms = [{
            $invalid: false, field: {
                $dirty: false, $setDirty: function () {
                    this.$dirty = true;
                }
            },
            innerForm: {
                $invalid: false
            }
        }];
    });

    it('sets currentLanguage', function () {
        expect($scope.currentLanguage).toEqual(lang);
    });

    it('sets forms dirty', function () {
        $scope.submitForm();
        expect($scope.forms[0].field.$dirty).toEqual(true);
    });

    it('saves on submit', function () {
        $scope.submitForm();
        expect($scope.objectEndpoint.save).toHaveBeenCalled();
    });

    it('updates on submit', function () {
        $scope.object = {id: 1};
        $scope.submitForm();
        expect($scope.objectEndpoint.update).toHaveBeenCalled();
    });

    it('deletes object', function () {
        $scope.object = {id: 1};
        var tmp = $window.confirm;
        $window.confirm = function (a) {
            return true;
        }; // remove so browser doesn't get stuck
        $scope.deleteObject();
        expect($scope.objectEndpoint.delete).toHaveBeenCalled();
        $window.confirm = tmp;
    });

    it('skips when forms invalid', function () {
        $scope.forms[0].$invalid = true;
        $scope.submitForm();
        expect($scope.objectEndpoint.save).not.toHaveBeenCalled();
    });

    it('adds onbeforeunload when object changes', function () {
        $scope.object = {id: 1};
        $rootScope.$apply();
        $scope.object = {id: 2};
        $rootScope.$apply();
        expect($window.onbeforeunload).not.toBeNull();
        expect($window.onbeforeunload().length).not.toEqual(0);
        $window.onbeforeunload = null; // remove so browser doesn't get stuck
    });

    it('adds onload function', function () {
        $rootScope.$apply();
        var result = $window.onload();
        expect(result).not.toBeNull();
        $window.onload = null; // remove so browser doesn't get stuck
    });

});


describe('glClientPaymentController', function () {
    var $rootScope;
    var $controller;
    var $injector;
    var $scope;
    var url = 'about:blank';

    beforeEach(function () {
        angular.module('gallant.services.glServices', []);
        module('gallant.services.glServices', function ($provide) {
            $provide.factory('$attrs', function ($q) {
                return {clientId: 0};
            });
            $provide.factory('ClientQuote', function ($q) {
                var ClientQuote = {};
                ClientQuote.query = function (a) { return {$promise: $q.when([{id: 0, client: 0, services: [{ cost: {amount: 0, currency: 'MXN'} }] }])}; };
                return ClientQuote;
            });
            $provide.factory('Client', function ($q) {
                var Client = {};
                Client.get = function (a) { return {$promise: $q.when({id: 0, currency: 'MXN'})}; };
                return Client;
            });
            $provide.factory('Payment', function ($q) {
                var Payment = {};
                Payment.query = function (a) { return {$promise: $q.when([{}])}; };
                Payment.get = function (a) { return {$promise: $q.when({id: 0, amount: {currency: '', amount: null}})}; };
                Payment.save = function (a) { return {}; };
                Payment.update = function (a) { return {}; };
                Payment.delete = function (a) { return {}; };
                return Payment;
            });
            $provide.factory('$uibModalInstance', function ($q) {
               return { dismiss: function(a) {} };
            });
            $provide.factory('createPayment', function ($q) {
               return {};
            });
            $provide.factory('updatePayment', function ($q) {
               return {};
            });
        });
        module('gallant.controllers.glClientPaymentController', function ($provide) {
            $provide.value('$uibModal', {args: {}, open: function (a) { this.args = a; }});
        });

        inject(function (_$rootScope_, _$controller_, _$window_, _$injector_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $controller = _$controller_;
            $injector = _$injector_;
        });
    });

    var $scope;

     beforeEach(function () {
        $scope = $rootScope.$new();
        $controller('glClientPaymentController', {$scope: $scope});
        $scope.$apply();
     });

    it('opens modal', function () {
        var $uibModal = $injector.get('$uibModal');
        var $subScope = $scope.$new();
        spyOn($uibModal, 'open').and.callThrough();
        $scope.openEditModal();
        $controller($uibModal.args.controller, {$scope: $subScope});
        $scope.$digest();
        expect($uibModal.open).toHaveBeenCalled();
    });

    describe('uibModalController', function() {
        var $subScope;

        beforeEach(function() {
            var $uibModal = $injector.get('$uibModal');
            $subScope = $scope.$new();
            $scope.openEditModal(0);
            $controller($uibModal.args.controller, {$scope: $subScope});
            $scope.$digest();
        });

        it('loads quotes', function() {
            expect($subScope.quotes.length).toBe(1);
        });

        it('can validate quote has services', function () {
            var is_approved = $subScope.isApproved({status: 5});
            expect(is_approved).toBe(true);
        });

        it('can run updateCurrency', function() {
            $subScope.updateCurrency(0);
            $scope.$digest();
            expect($subScope.currency).toBe('( in MXN )')
        });

        it('can run openDueDatePicker', function() {
            $subScope.openDueDatePicker();
            $scope.$digest();
            expect($subScope.due_date_opened).toBe(true);
        });

        it('can run openPaidDatePicker', function () {
            $subScope.openPaidDatePicker();
            $scope.$digest();
            expect($subScope.paid_date_opened).toBe(true);
        });

        it('raises error for bogus payment', function () {
            $subScope.submit();
            $scope.$digest();
            expect($subScope.errors).toBeDefined();
        });

        it('cancels', function() {
            var $uibModalInstance = $injector.get('$uibModalInstance');
            spyOn($uibModalInstance, 'dismiss');
            $subScope.cancel();
            $scope.$digest();
            expect($uibModalInstance.dismiss).toHaveBeenCalled();
        });

        it('can submit form', function () {
            var Payment = $injector.get('Payment');
            $subScope.payment = {
                quote: 0,
                amount: {amount: 1.0, currency: 'MXN'},
                description: 'Payment',
                due: new Date(),
                paid_on: new Date(),
                notes: []
            };
            $subScope.createPayment = $scope.createPayment;
            spyOn(Payment, 'save').and.callThrough();
            $subScope.submit();
            $scope.$digest();
            expect(Payment.save).toHaveBeenCalled();
        });

        it('can update payment', function () {
            var Payment = $injector.get('Payment');
            $subScope.payment.id = 1;
            $subScope.payment.description = 'Payment';
            $subScope.payment.quote = 0;
            $subScope.payment.amount.amount = 1.0;
            $subScope.payment.amount.currency = 'MXN';
            $subScope.updatePayment = $scope.updatePayment;
            spyOn(Payment, 'update').and.callThrough();
            $subScope.submit();
            $scope.$digest();
            expect(Payment.update).toHaveBeenCalled();
        });

    });

});

describe('glUserDashboardController', function () {
    var $rootScope;
    var $controller;
    var $window;
    var url = 'about:blank';

    beforeEach(function () {
        module('gallant.controllers.glUserDashboardController', function ($provide) {
            $provide.factory('UserSettings', function ($q) {
                return {
                    get: function() { return {$promise: $q.when({settings: {}})}; },
                };
            });
        });

        inject(function (_$rootScope_, _$controller_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $controller = _$controller_;
        });
    });

    var $scope;

    beforeEach(function () {
        $scope = $rootScope.$new();
        $scope.openDashOnboarding = jasmine.createSpy('openDashOnboarding');
        $controller('glUserDashboardController', {$scope: $scope});
        $scope.init(1, true);
        $rootScope.$apply();
    });

    it('opens onboarding', function () {
        expect($scope.openDashOnboarding).toHaveBeenCalled();
    });

    it('updates user', function () {
        $scope.user.$update = jasmine.createSpy('$update');
        $scope.saveSettings();
        $scope.$apply();
        expect($scope.user.$update).toHaveBeenCalled();
    });
});
