var app = angular.module('gallant.controllers.glClientPaymentController', [])

app.controller('glClientPaymentController', function ($scope, $attrs, $uibModal, $log, ClientProjects, ClientQuoteDetail) {
    $scope.openEditModal = function (payment) {
        $uibModal.open({
            templateUrl: '/static/gallant/html/gl_client_payment_modal.html',
            backdrop: true,
            windowClass: 'modal',
            controller: function ($scope) {
                $scope.cancel = function () {
                    $modalInstance.dismiss('cancel');
                };

                $scope.dt = new Date();
                $scope.projects = [];
                $scope.currency = "";

                $scope.getProjects = function () {
                    ClientProjects.query({id: $attrs.clientId}).$promise.then(function (response) {
                        $scope.projects = response;
                    });
                };

                $scope.getProjects();

                $scope.openDueDatePicker = function () {
                    $scope.due_date_opened = true;
                };

                $scope.openPaidDatePicker = function () {
                    $scope.paid_date_opened = true;
                };

                $scope.updateCurrency = function(project) {
                    console.log($scope.projects);
                }

                $scope.ok = function () {
                    $modalInstance.close($scope.dt);
                };
            },
            resolve: {}
        });
    };

});