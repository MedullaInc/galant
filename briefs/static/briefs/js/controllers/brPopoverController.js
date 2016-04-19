app = angular.module('briefs.controllers.brPopoverController', ['ngAnimate', 'ui.bootstrap', 'briefs.services.brServices']);

app.controller('brPopoverController', ['$scope', '$http', '$window', '$rootScope', '$uibModal', 'Brief', 'BriefTemplate',
    function ($scope, $http, $window, $rootScope, $uibModal, Brief, BriefTemplate) {

        if ($rootScope.briefTemplates) {
            $scope.briefTemplates = $rootScope.briefTemplates;
        } else {
            BriefTemplate.query().$promise.then(function (response) {
                $scope.briefTemplates = response;
            });
        }

        $scope.init = function (addBriefUrl, currentLanguage, clientId) {
            $scope.addBriefUrl = addBriefUrl;
            $scope.currentLanguage = currentLanguage;
            $scope.selectedLanguage = currentLanguage;
            $scope.clientId = clientId;
        };

        $scope.dynamicPopover = {
            templateUrl: 'addBriefPopoverTemplate.html',
        };

        $scope.redirectTemplate = function (briefTemplate) {
            // In case there was no selection
            if (!briefTemplate.languageSelection) {
                briefTemplate.languageSelection = $scope.currentLanguage;
            }
            var ref = $scope.addBriefUrl + "?template_id=" + briefTemplate.id + "&lang=" + briefTemplate.languageSelection;
            if ($scope.clientId)
                ref += '&client_id=' + $scope.clientId;
            $window.location.href = ref;
        };

        $scope.addBriefRedirect = function () {
            var ref = $scope.addBriefUrl;
            if ($scope.clientId)
                ref += '?client_id=' + $scope.clientId;
            $window.location.href = ref;
        };

        $scope.languageSelection = function (briefTemplate, lang) {
            briefTemplate.languageSelection = lang;
        };

        $scope.open = function () {
            $scope.modalInstance = $uibModal.open({
                scope: $scope,
                animation: true,
                templateUrl: 'briefTemplateModalContent.html',
                controller: 'brPopoverController',
            });
            return 0;
        };

    }

]);