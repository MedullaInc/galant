describe('brForm', function () {
    var $rootScope;
    var $compile;
    var $scope;

    beforeEach(function () {
        module('briefs.directives.brForm');
        module('staticNgTemplates');

        angular.module('brief.services.brServices', []);
        module('brief.services.brServices', function ($provide) {
            $provide.factory('Question', function ($q) {
                var Question = function () { return {id: 0}; };
                Question.get = function () { return {$promise: $q.when([{id: 0}])}; };
                return Question;
            });

            $provide.factory('Brief', function ($q) {
                var Brief = function () { return {id: 0}; };
                Brief.get = function () { return {$promise: $q.when({id: 0})}; };
                return Brief;
            });

            $provide.factory('BriefTemplate', function ($q) {
                var BriefTemplate = function () {};
                BriefTemplate.get = function () { return {$promise: $q.when({id: 0, brief: {
                    id: 0,
                    questions: [{}]
                }})}; };
                return BriefTemplate;
            });
        });

        inject(function (_$rootScope_, _$compile_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $compile = _$compile_;
        });

        $scope = $rootScope.$new();
    });

    describe('brQuestionForm', function () {
        beforeEach(function () {
            $scope.question = {type: 'TextQuestion'};
            $scope.language = 'en';
        });

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

        it('removes question', function () {
            $scope.removeQuestion = function () { $scope.question = null; };
            var element = $compile(
                '<div br-question-form question="question" remove-question="removeQuestion"></div>'
            )($scope);
            $scope.$digest();

            var tmp = window.confirm;
            window.confirm = function (str) { return true; };

            element.isolateScope().remove();
            window.confirm = tmp;

            expect($scope.question).toBeNull();
        });

        it('adds and removes choices', function () {
            $scope.question.choices = [];
            var element = $compile('<div br-question-form question="question"></div>')($scope);
            $scope.$digest();

            element.isolateScope().addChoice();
            expect($scope.question.choices.length).toEqual(1);

            var tmp = window.confirm;
            window.confirm = function (str) { return true; };
            element.isolateScope().removeChoice(0);
            window.confirm = tmp;
            expect($scope.question.choices.length).toEqual(0);
        });
    });

    describe('brBriefForm', function () {
        it('compiles', function () {
            var element = $compile('<div br-brief-form></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 8)).toEqual('<ng-form');
        });

        it('compiles with brief id', function () {
            var element = $compile('<div br-brief-form brief-id="0"></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 8)).toEqual('<ng-form');
        });

        it('compiles with brief template id', function () {
            var element = $compile('<div br-brief-form template-id="0" quote-id="0" client-id="0"></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 8)).toEqual('<ng-form');
        });
    });
});
