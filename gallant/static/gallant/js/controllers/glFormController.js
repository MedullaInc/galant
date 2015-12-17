app = angular.module('gallant.controllers.glFormController', []);

app.controller('glFormController', ['$scope', '$http', '$window',
    function ($scope, $http, $window) {

        var setFormsDirty = function (forms) {
            var valid = true;
            var inner = [];

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
                if ($scope.object.id) {
                    method = $scope.objectEndpoint.update;
                } else {
                    method = $scope.objectEndpoint.save;
                }

                method({id: $scope.object.id}, $scope.object, function (response) {
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

        $scope.$watch('object', function (newValue, oldValue) {
            if (oldValue !== null && newValue != oldValue) {
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