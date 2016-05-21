describe('glServices', function () {
    var $rootScope;
    var validate;
    var alert;
    var $scope;

    beforeEach(function () {
        angular.module('ngResource', []);
        module('gallant.services.glServices');

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

    describe('glAlertService', function () {
        beforeEach(angular.mock.inject(function(_glAlertService_) {
            alert = _glAlertService_;
            alert.add({type:'success', msg:'0'});
        }));

        it('adds alert', function () {
            alert.add({type:'success', msg:'msg'});
            expect(alert.get().length).toEqual(2);
        });

        it('closes alert', function () {
            var a = {type:'success', msg:'msg'};
            alert.add(a);
            alert.closeAlert(a);
            expect(alert.get().length).toEqual(0);
        });

        it('clears alerts', function () {
            alert.clear();
            expect(alert.get().length).toEqual(0);
        });
    });
});
