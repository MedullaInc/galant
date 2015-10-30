angular.module('briefs.controllers.briefFormController', [])
    .controller('briefFormController', ['$scope', 'Brief',
        function ($scope, Brief) {
            var setFormsDirty = function (forms) {
                valid = true;
                inner = [];

                angular.forEach(forms, function (form) {
                        if (!form) {
                            return;
                        }
                        angular.forEach(form, function (val, key) {
                                if (key.match(/innerForm/)) { // support nested forms with this name
                                    inner.push(val);
                                } else if (!key.match(/\$/)) {
                                    val.$setDirty();
                                }
                            }
                        );
                        valid = valid && !form.$invalid;
                    }
                );

                if (inner.length > 0) {
                    var ret = setFormsDirty(inner);
                    valid = valid && ret;
                }
                return valid;
            };

            $scope.submitForm = function () {
                var valid = setFormsDirty($scope.forms);

                if (valid) {
                    console.log($scope);
                    Brief.update({id: $scope.brief.id}, $scope.brief, function (response) {
                        if (response.redirect) {
                            window.location.href = response.redirect;
                        } else {
                            // handle errors
                            var errors = response.errors[0];
                            console.log(errors);
                        }
                    }, function (errorResponse) {
                        console.log(errorResponse.data);
                    });
                }
            };

            $scope.init = function (currentLanguage) {
                $scope.currentLanguage = currentLanguage;
            };
        }
    ]);