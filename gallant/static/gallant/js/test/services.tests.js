describe('glServices', function () {
    var $rootScope;
    var validate;
    var $scope;

    beforeEach(function () {
        angular.module('ngResource', []);
        angular.mock.module('gallant.services.glServices');

        inject(function (_$rootScope_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
        });

        $scope = $rootScope.$new();
    });

    describe('glValidateErrors', function () {
        beforeEach(angular.mock.inject(function(_glValidate_) {
            validate = _glValidate_;
        }));
        it('validates data', function () {
            var err = validate.nonEmpty('');
            expect(!err);
            var err = validate.selected('');
            expect(!err);
            var err = validate.selectedIf('', false);
            expect(!err);
        });
    });
});
