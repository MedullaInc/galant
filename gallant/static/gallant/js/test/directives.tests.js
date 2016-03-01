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
