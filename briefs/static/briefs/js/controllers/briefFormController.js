angular.module('briefs.controllers.briefFormController', [])
    .controller('briefFormController', ['$scope', '$http', '$window', 'Brief',
        function ($scope, $http, $window, Brief) {
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
                    $window.onbeforeunload = null;
                    var method = null;
                    if ($scope.brief.id) {
                        method = Brief.update;
                    } else {
                        method = Brief.save;
                    }

                    method({id: $scope.brief.id}, $scope.brief, function (response) {
                        if (response.redirect) {
                            window.location.href = response.redirect;
                        } else {
                            // handle errors
                            console.log(JSON.stringify(response.data));
                        }
                    }, function (errorResponse) {
                        console.log(JSON.stringify(errorResponse.data));
                    });
                }
            };

            $scope.init = function (currentLanguage, csrftoken) {
                $scope.currentLanguage = currentLanguage;
                $http.defaults.headers.post['X-CSRFToken'] = csrftoken;
            };

            $scope.$watch('brief', function (newValue, oldValue) {
                if (oldValue != null && newValue != oldValue) {
                    if (!$window.onbeforeunload) {
                        $window.onbeforeunload = function (e) {
                            // If we haven't been passed the event get the window.event
                            e = e || $window.event;
                            var message = 'You have unsaved changes. If you leave this page they will be lost.';

                            // For IE6-8 and Firefox prior to version 4
                            if (e) {
                                e.returnValue = message;
                            }
                            return message;
                        };
                    }
                }
            }, true);
        }
    ]);