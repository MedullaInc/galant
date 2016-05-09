app = angular.module('gallant.controllers.glFormController', ['gallant.services.glServices']);

app.controller('glFormController', ['$scope', '$http', '$window', 'glAlertService',
    function ($scope, $http, $window, glAlertService) {
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
                var method = null;
                if ($scope.object.id) {
                    method = $scope.objectEndpoint.update;
                } else {
                    method = $scope.objectEndpoint.save;
                }

                method({id: $scope.object.id}, $scope.object, function (response) {
                    $window.onbeforeunload = null;
                    if (response.redirect) {
                        window.location.href = response.redirect;
                    } else {
                        glAlertService.add('success', 'Saved.');

                        if ($scope.onaftersave)
                            $scope.onaftersave(response);
                    }
                }, /* istanbul ignore next */ function (errorResponse) {
                    $scope.object.errors = errorResponse.data;
                    // glAlertService.add('danger', 'Error: ' + JSON.stringify(errorResponse.data));
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
                        glAlertService.add('danger', 'Server returned error.');
                    }
                }, /* istanbul ignore next */ function (errorResponse) {
                    glAlertService.add('danger', 'Server returned error.');
                });
            }
        };

        $scope.init = function (currentLanguage, csrftoken, onaftersave) {
            $scope.currentLanguage = currentLanguage;
            if (csrftoken)
                $http.defaults.headers.post['X-CSRFToken'] = csrftoken;
            $scope.onaftersave = onaftersave;
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