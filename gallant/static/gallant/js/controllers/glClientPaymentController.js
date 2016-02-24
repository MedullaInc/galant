app = angular.module('gallant.controllers.glClientPaymentController', ['gallant.services.glServices']);

app.controller('glClientPaymentController', ['$scope', '$attrs', '$uibModal', '$log', 'ClientProjects', '$http', '$window', 'PaymentAPI', function ($scope, $attrs, $uibModal, $log, ClientProjects, $http, $window, PaymentAPI) {
    $scope.openEditModal = function () {
        $uibModal.open({
            templateUrl: '/static/gallant/html/gl_client_payment_modal.html',
            backdrop: true,
            windowClass: 'modal',
            controller: function ($scope, $uibModalInstance, ClientProjects, createPayment, PaymentAPI) {

                // When form loads, it will load projects
                $scope.projects = [];

                // Load default payment formant & due date
                $scope.payment = {amount: {currency: '', amount: null}};
                $scope.payment.due = new Date();

                $scope.getProjects = function () {
                    ClientProjects.query({id: $attrs.clientId}).$promise.then(function (response) {
                        $scope.projects = response;
                    });
                };

                $scope.getProjects();

                // When selecting a project, currency will update as well as quote
                $scope.updateCurrency = function (project_id) {
                    $scope.payment.amount.currency = $.grep($scope.projects, function (e) {
                        return e.id == project_id
                    })[0].payments.currency;
                    $scope.currency = '( in ' + $.grep($scope.projects, function (e) {
                            return e.id == project_id
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
                $scope.submit = function () {
                    if (typeof $scope.payment == 'undefined' || typeof $scope.payment.project_id == 'undefined' || typeof $scope.payment.amount.amount == 'undefined' || $scope.payment.amount.amount <= 0.0 || typeof $scope.payment.description == 'undefined' ) {
                        $scope.errors = "Project, Amount & Description are required!";
                    } else {
                        $scope.errors = "";
                        // TODO: Change form to ng-model='amount.amount'
                        $scope.createPayment($scope.payment);
                        $uibModalInstance.dismiss('close');
                    }
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
        var newPayment = {
            project_id: payment.project_id,
            amount: payment.amount,
            description: payment.description,
            due: payment.due,
            paid_on: payment.paid_on,
            notes: []
        };

        newPayment.amount.amount = parseFloat(payment.amount.amount);

        $scope.postPayment(newPayment);

    };

    $scope.postPayment = function (payment) {
        var response = PaymentAPI.save(payment);
        $scope.renderPayment(response);
    };

    $scope.renderPayment = function (response) {
        // Load payments into view
    };

}]);