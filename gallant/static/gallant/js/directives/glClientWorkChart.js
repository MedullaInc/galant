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

            Service.query({client_id: $scope.clientId}).$promise.then(function (response) {
            });
            
            $scope.work_data = [
                {
                    value: 1,
                    color: "#02ff02",
                    highlight: "#afff93",
                    label: "Paid"
                },
                {
                    value: 2,
                    color: "#ff022c",
                    highlight: "#FF5A5E",
                    label: "Overdue"
                },
                {
                    value: 3,
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
            $scope.work_options = {

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
    };
}]);