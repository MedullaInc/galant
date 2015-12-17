describe('glForm', function () {
    var $rootScope;
    var $compile;

    beforeEach(function () {
        module('gallant.directives.glForm');
        module('staticNgTemplates');

        inject(function (_$rootScope_, _$compile_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $compile = _$compile_;
        });
    });

    describe('glRequiredErrors', function () {
        it('compiles', function () {
            var element = $compile("<div gl-required-errors></div>")($rootScope);
            $rootScope.$digest();
            expect(element.html().substring(0,3)).toEqual('<ul');
        });
    });
});
