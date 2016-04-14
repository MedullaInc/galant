app = angular.module('gallant.directives.glClientMoneyChart', [
    'gallant.services.glServices',
    'tc.chartjs',
]);

app.directive('glClientMoneyChart', ['$window', 'Payment', function ($window, Payment) {
    return {
        restrict: 'A',
        scope: {
            addQuoteUrl: '@',
            language: '@',
            clientId: '@'
        },
        controller: ['$scope', function ($scope) {
        }],
        templateUrl: '/static/gallant/html/gl_client_money_chart.html',
        link: function ($scope) {

            $scope.payments = [];
            $scope.paid    = 0.0;
            $scope.overdue = 0.0;
            $scope.pending = 0.0;
            $scope.on_hold = 0.0;

            Payment.query({client_id: $scope.clientId}).$promise.then(function (response) {
                $scope.payments = response;

                if ($scope.payments.length > 0) {

                    for (var i = 0; i < $scope.payments.length; i++) {
                        if ($scope.payments[i].paid_on != null) {
                            $scope.paid += parseFloat($scope.payments[i].amount.amount);
                        } else if (new Date($scope.payments[i].due) < new Date()) {
                            $scope.overdue += parseFloat($scope.payments[i].amount.amount);
                        } else if (new Date($scope.payments[i].due) > new Date()) {
                            $scope.pending += parseFloat($scope.payments[i].amount.amount);
                        } else {
                            $scope.on_hold += parseFloat($scope.payments[i].amount.amount);
                        }
                    }

                    $scope.money_data = [
                        {
                            value: $scope.paid,
                            color: "#02ff02",
                            highlight: "#afff93",
                            label: "Paid"
                        },
                        {
                            value: $scope.overdue,
                            color: "#ff022c",
                            highlight: "#FF5A5E",
                            label: "Overdue"
                        },
                        {
                            value: $scope.pending,
                            color: "#02deff",
                            highlight: "#93f1ff",
                            label: "Pending"
                        },
                        //{
                        //    value: $scope.on_hold,
                        //    color: "#999999",
                        //    highlight: "#FFC870",
                        //    label: "On Hold"
                        //}
                    ];

                    // Chart.js Options
                    $scope.money_options = {

                        // Sets the chart to be responsive
                        responsive: true,

                        //Boolean - Whether we should show a stroke on each segment
                        segmentShowStroke: true,

                        //String - The colour of each segment stroke
                        segmentStrokeColor: '#ffffff',

                        //Number - The width of each segment stroke
                        segmentStrokeWidth: 0,

                        //Number - The percentage of the chart that we cut out of the middle
                        percentageInnerCutout: 50, // This is 0 for Pie charts

                        //Number - Amount of animation steps
                        animationSteps: 100,

                        //String - Animation easing effect
                        animationEasing: 'easeOutBounce',

                        //Boolean - Whether we animate the rotation of the Doughnut
                        animateRotate: true,

                        //Boolean - Whether we animate scaling the Doughnut from the centre
                        animateScale: false,

                        //String - A legend template
                        legendTemplate: '<ul class="tc-chart-js-legend"><% for (var i=0; i<segments.length; i++){%><li><span style="background-color:<%=segments[i].fillColor%>"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>'

                    };
                }
            });
        }
    };
}]);