app = angular.module('gallant.controllers.glClientPaymentController', []);

app.controller('glClientPaymentController', ['$scope', '$attrs', '$uibModal', '$log', 'ClientProjects', '$http', '$window', function ($scope, $attrs, $uibModal) {
    $scope.openEditModal = function () {
        $uibModal.open({
            templateUrl: '/static/gallant/html/gl_client_payment_modal.html',
            backdrop: true,
            windowClass: 'modal',
            controller: function ($scope, $uibModalInstance, ClientProjects, createPayment) {

                // When form loads, it will load projects
                $scope.projects = [];

                $scope.getProjects = function () {
                    ClientProjects.query({id: $attrs.clientId}).$promise.then(function (response) {
                        $scope.projects = response;
                    });
                };

                $scope.getProjects();

                // When selecting a project, currency will update
                $scope.updateCurrency = function (project) {
                    $scope.currency = '( in ' + $.grep($scope.projects, function (e) {
                            return e.id == project
                        })[0].payments.currency + ' )';
                    if ($scope.currency == '( in  )') {
                        $scope.currency = '( N/A )'
                    }
                };

                // Date pickers
                $scope.openDueDatePicker = function () {
                    $scope.due_date_opened = true;
                };

                $scope.openPaidDatePicker = function () {
                    $scope.paid_date_opened = true;
                };

                // Form functions
                $scope.createPayment = createPayment;
                $scope.submit = function (e) {
                    var newPayment = {
                        "id": "",
                        "quote": payment.quote,
                        "amount": payment.amount,
                        "description": payment.description,
                        "due": moment(payment.due).format(),
                        "paid_on": moment(payment.paid_on).format()
                    };
                    
                    $scope.createPayment(newPayment);
                };

                // Modal functions
                $scope.cancel = function () {
                    $uibModalInstance.dismiss('cancel');
                };

            },
            resolve: {
                createPayment: function () {
                    return $scope.createPayment;
                },
            }
        });
    };

    $scope.createPayment = function (payment) {
        console.log("OK");
    };


}]);