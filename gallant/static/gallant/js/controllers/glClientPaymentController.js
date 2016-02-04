app = angular.module('gallant.controllers.glClientPaymentController', ['ui.bootstrap', 'ng.django.forms']);

app.controller('glClientPaymentController', ['$scope', '$attrs', '$uibModal', '$log', 'ClientProjects', '$http', '$window', function ($scope, $attrs, $uibModal, Payment) {
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
                $scope.submit = function () {
                    if (typeof $scope.payment == 'undefined' || typeof $scope.payment.quote == 'undefined' || typeof $scope.payment.amount == 'undefined' || typeof $scope.payment.description == 'undefined' ) {
                        $scope.errors = "Project, Amount & Description are required!";
                    } else {
                        $scope.errors = "";
                        $scope.createPayment($scope.payment);
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
            'quote': payment.quote,
            'amount': payment.amount,
            'description': payment.description,
            'due': new Date(payment.due),
            'paid_on': new Date(payment.paid_on)
        };

        $scope.postPayment(newPayment);

    };

    $scope.postPayment = function (payment) {
        Payment.save({payment: payment}).$promise.then(function (response) {
            $scope.renderPayment(response);
        });
    };

    $scope.renderPayment = function (response) {
        console.log(response);
    };

}]);