describe('glDeliverableAdd', function () {
    var $rootScope;
    var $compile;
    var $scope;

    beforeEach(function () {
        module('gallant.services.glServices', function ($provide) {
            $provide.factory('Project', function ($q) {;
                return {};
            });

            $provide.factory('Service', function ($q) {
                return function () {
                };
            });
        });

        module('gallant.directives.glDeliverableAdd', function ($controllerProvider) {
            $controllerProvider.register('glFormController', function ($scope) {
                // Controller Mock
            });
        });

        module('staticNgTemplates');

        inject(function (_$rootScope_, _$compile_, _$injector_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $compile = _$compile_;
        });

        $scope = $rootScope.$new();
    });

    var element;

    beforeEach(inject(function () {
        $scope.project = {services: [{id: 1}]};
        element = $compile('<div gl-deliverable-add project="project"></div>')($scope);
        $scope.$digest();
    }));

    it('compiles', function () {
        expect(element.html().substring(0, 6)).toEqual('<form ');
    });

    it('saves deliverable', function () {
        element.isolateScope().saveDeliverable();
        $scope.$digest();
        expect(element.isolateScope().project.services.length).toEqual(2);
    });

    it('deletes deliverable', function () {
        element.isolateScope().saveDeliverable();
        element.isolateScope().deleteDeliverable({id: 1});
        $scope.$digest();
        expect(element.isolateScope().project.services.length).toEqual(1);
    });
});
