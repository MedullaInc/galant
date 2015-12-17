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
        $scope.question = {type: 'TextQuestion'};
        $scope.language = 'en';
    });

    describe('brQuestionForm', function () {
        it('compiles', function () {
            var element = $compile('<div br-question-form question="question"></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 3)).toEqual('<!-');
        });

        it('sets question text', function () {
            var element = $compile('<div br-question-form question="question" language="language"></div>')($scope);
            $scope.$digest();

            var q = angular.element(element.find('input')[1]);
            q.val('Huh?').triggerHandler('input');

            expect($scope.question.question[$scope.language]).toEqual('Huh?');
        });

        it('sets multiquestion text', function () {
            $scope.question.type = 'MultipleChoiceQuestion';
            var element = $compile('<div br-question-form question="question" language="language"></div>')($scope);
            $scope.$digest();

            var q = angular.element(element.find('input')[1]);
            q.val('Huh?').triggerHandler('input');

            expect($scope.question.question[$scope.language]).toEqual('Huh?');
        });

        it('sets multiquestion select multiple', function () {
            $scope.question.type = 'MultipleChoiceQuestion';
            $scope.question.can_select_multiple = false;
            var element = $compile('<div br-question-form question="question" language="language"></div>')($scope);
            $scope.$digest();

            var q = angular.element(element.find('input')[0]);
            q.prop('checked', true).triggerHandler('click');

            expect($scope.question.can_select_multiple).toEqual(true);
        });
    });
});
