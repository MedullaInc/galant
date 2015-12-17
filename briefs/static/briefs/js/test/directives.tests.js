describe('brForm', function () {
    var $rootScope;
    var $compile;
    var $scope;

    beforeEach(function () {
        module('briefs.directives.brForm');
        module('staticNgTemplates');

        inject(function (_$rootScope_, _$compile_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $compile = _$compile_;
        });

        $scope = $rootScope.$new();
    });

    describe('brQuestionForm', function () {
        it('compiles', function () {
            $rootScope.question = {type: 'MultipleChoiceQuestion'};
            var element = $compile('<div br-question-form question="question"></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 3)).toEqual('<!-');
        });
    });
});
