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
                    /* istanbul ignore else  */
                    if (response.redirect) {
                        window.location.href = response.redirect;
                    } else {
                        // handle errors
                        console.log(JSON.stringify(response.data));
                    }
                }, /* istanbul ignore next */ function (errorResponse) {
                    $scope.object.errors = errorResponse.data;
                    console.log(JSON.stringify(errorResponse.data));
                });
            }
        };

        $scope.deleteObject = function (objectType) {
            if ($window.confirm("Are you sure you want to delete this " + objectType + "?")) {
                $scope.objectEndpoint.delete({id: $scope.object.id}, function (response) {
                    /* istanbul ignore else  */
                    if (response.redirect) {
                        window.location.href = response.redirect;
                    } else {
                        // handle errors
                        console.log(JSON.stringify(response.data));
                    }
                }, /* istanbul ignore next */ function (errorResponse) {
                    console.log(JSON.stringify(errorResponse.data));
                });
            }
        };

        $scope.init = function (currentLanguage, csrftoken) {
            $scope.currentLanguage = currentLanguage;
            $http.defaults.headers.post['X-CSRFToken'] = csrftoken;
        };

        $window.onload = function (e) {
            $scope.startTime = new Date();
        }

        $scope.$watch('object', function (newValue, oldValue) {
            if ((oldValue !== null && typeof(oldValue) !== 'undefined') && newValue != oldValue) {
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