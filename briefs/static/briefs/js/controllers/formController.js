angular.module('briefs.controllers.briefFormController', ['ng.django.forms'])
  .controller('briefFormController', function ($scope, $http) {
    $scope.submitForm = function () {
        debugger;
        var valid = true;
        angular.forEach(forms, function (form) {
            form.$setDirty();
            valid = valid && !form.$invalid;
        });

        // var data = {csrfmiddlewaretoken: '{{csrf_token}}'};

        for (var k in $scope.brief) {
            data['brief.' + k] = $scope.brief[k];
        }
        for (var prefix in $scope.question_forms) {
            for (var k in $scope.question_forms[prefix]) {
                data[prefix + '.' + k] = $scope.question_forms[prefix][k];
            }
        }

        if (valid) {
            $.post('', data, function (response) {
                if (response.redirect) {
                    window.location.href = response.redirect;
                } else {
                    // handle errors
                    var errors = response.errors[0];
                    console.log(errors);
                }
            });
        }
    }

    $scope.init = function (currentLanguage, brief_id) {
        if (brief_id) {
            // TODO: change URL structure to /api/ instead of /en/blabla/api
            $http.get("/en/briefs/api/brief/" + brief_id)
                .success(function (response) {
                    $scope.brief = response;
                });
        }

        $scope.currentLanguage = currentLanguage;
    }
});