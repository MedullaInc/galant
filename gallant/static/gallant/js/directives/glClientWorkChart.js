app = angular.module('gallant.directives.glClientWorkChart', [
    'gallant.services.glServices',
    'tc.chartjs',
]);

app.directive('glClientWorkChart', ['$window', 'Service', function ($window, Service) {
    return {
        restrict: 'A',
        scope: {
            clientId: '@',
        },
        controller: ['$scope', function ($scope) {
        }],
        templateUrl: '/static/gallant/html/gl_client_work_chart.html',
        link: function ($scope) {

            $scope.work = [];
            $scope.on_hold = 0;
            $scope.pending = 0;
            $scope.active = 0;
            $scope.overdue = 0;
            $scope.completed = 0;

            Service.query({client_id: $scope.clientId}).$promise.then(function (response) {
                $scope.work = response;

                if ($scope.work.length > 0) {
                    for (var i = 0; i < $scope.work.length; i++) {
                        if ($scope.work[i].status == 0) {
                            $scope.on_hold += 1;
                        } else if ($scope.work[i].status == 1) {
                            $scope.pending += 1;
                        } else if ($scope.work[i].status == 2) {
                            $scope.active += 1;
                        } else if ($scope.work[i].status == 3) {
                            $scope.overdue += 1;
                        } else if ($scope.work[i].status == 4) {
                            $scope.completed += 1;
                        }
                    }

                    $scope.work_data = [
                        {
                            value: $scope.pending,
                            color: '#ffa861',
                            highlight: '#ff7300',
                            label: "Pending"
                        },
                        {
                            value: $scope.active,
                            color: "#93f1ff",
                            highlight: "#00a6ff",
                            label: "Active"
                        },
                        {
                            value: $scope.overdue,
                            color: "#ff0054",
                            highlight: "#FF5A5E",
                            label: "Overdue"
                        },
                        {
                            value: $scope.on_hold,
                            color: "#d9ff03",
                            highlight: "#f3ffb1",
                            label: "On Hold"
                        },
                        {
                            value: $scope.completed,
                            color: '#b2ffaf',
                            highlight: '#00ff5f',
                            label: "Completed"
                        }
                    ];

                    // Chart.js Options
                    $scope.work_options = {

                        // Sets the chart to be responsive
                        responsive: true,

                        //Boolean - Whether we should show a stroke on each segment
                        segmentShowStroke: true,

                        //String - The colour of each segment stroke
                        segmentStrokeColor: '#ffffff',

                        //Number - The width of each segment stroke
                        segmentStrokeWidth: 5,

                        //Number - The percentage of the chart that we cut out of the middle
                        percentageInnerCutout: 70, // This is 0 for Pie charts

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