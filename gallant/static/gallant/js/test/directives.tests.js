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
    });

    describe('glUltextArea', function () {
        it('compiles', function () {
            var element = $compile('<div gl-ultext-area></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 3)).toEqual('<te');
        });
    });
});
