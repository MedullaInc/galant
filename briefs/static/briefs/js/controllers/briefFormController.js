angular.module('briefs.controllers.briefFormController', [])
    .controller('briefFormController', ['$scope',
        function ($scope) {

            $scope.submitForm = function () {
                debugger;
                var valid = true;
                angular.forEach($scope.forms, function (form) {
                    form.$setDirty();
                    valid = valid && !form.$invalid;
                });

                // var data = {csrfmiddlewaretoken: '{{csrf_token}}'};

                if (valid) {
                    $.post('', $scope.brief, function (response) {
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

            $scope.init = function (currentLanguage) {
                $scope.currentLanguage = currentLanguage;
            }
        }]);