app = angular.module('gallant.directives.glDashboardWorkSummary', [
    'gallant.services.glServices',
    'tc.chartjs',
]);

app.directive('glDashboardWorkSummary', ['$window', 'Client', 'ClientProjects', function ($window, Client, ClientProjects) {
    return {
        restrict: 'A',
        scope: true,
        controller: ['$scope', function ($scope) {
        }],
        templateUrl: '/static/gallant/html/gl_dashboard_work_summary.html',
        link: function ($scope) {

            $scope.potential_clients = 0;
            $scope.quoted_clients = 0;
            $scope.project_underway = [];

            $scope.service_on_hold = 0;
            $scope.service_pending_assignment = 0;
            $scope.service_active = 0;
            $scope.service_overdue = 0;
            $scope.service_completed = 0;

            Client.query().$promise.then(function (response) {
                angular.forEach(response, function (client) {
                    $scope.potential_clients += client.status == 0 ? 1 : 0;
                    $scope.quoted_clients += client.status == 1 ? 1 : 0;

                    if (client.status == 2) {
                        $scope.project_underway.push(client)
                    }

                });

                $scope.work_polar_chart_data = [];

                if ($scope.potential_clients > 0) {
                    $scope.work_polar_chart_data.push(
                        {
                            value: $scope.potential_clients,
                            color: "#93f1ff",
                            highlight: "#00a6ff",
                            label: 'Potential Clients'
                        }
                    );
                }

                if ($scope.quoted_clients > 0) {
                    $scope.work_polar_chart_data.push(
                        {
                            value: $scope.quoted_clients,
                            color: '#ffa861',
                            highlight: '#ff7300',
                            label: 'Quoted Clients'
                        }
                    );
                }

                if ($scope.project_underway.length > 0) {
                    $scope.work_polar_chart_data.push(
                        {
                            value: $scope.project_underway.length,
                            color: '#b2ffaf',
                            highlight: '#00ff5f',
                            label: 'Project Underway'
                        }
                    );
                }

                angular.forEach($scope.project_underway, function (client) {

                    ClientProjects.query({id: client.id}).$promise.then(function (response) {
                        angular.forEach(response, function (project) {
                            // If project is not completed
                            if (project.status != 4) {
                                angular.forEach(project.services, function (service) {
                                    $scope.service_on_hold += service.status == 0 ? 1 : 0;
                                    $scope.service_pending_assignment += service.status == 1 ? 1 : 0;
                                    $scope.service_active += service.status == 2 ? 1 : 0;
                                    $scope.service_overdue += service.status == 3 ? 1 : 0;
                                    $scope.service_completed += service.status == 4 ? 1 : 0;
                                });
                            }
                        });

                        $scope.work_doughnut_chart_data = [];

                        if ($scope.service_on_hold + $scope.service_pending_assignment > 0) {
                            $scope.work_doughnut_chart_data.push(
                                {
                                    value: $scope.service_on_hold + $scope.service_pending_assignment,
                                    color: "#93f1ff",
                                    highlight: "#00a6ff",
                                    label: "On Hold or Pending Assignment"
                                }
                            );
                        }

                        if ($scope.service_active > 0) {
                            $scope.work_doughnut_chart_data.push(
                                {
                                    value: $scope.service_active,
                                    color: '#b2ffaf',
                                    highlight: '#00ff5f',
                                    label: "Active"
                                }
                            );
                        }

                        if ($scope.service_overdue > 0) {
                            $scope.work_doughnut_chart_data.push(
                                {
                                    value: $scope.service_overdue,
                                    color: "#ff0054",
                                    highlight: "#FF5A5E",
                                    label: "Overdue"
                                }
                            );
                        }

                        if ($scope.service_completed > 0) {
                            $scope.work_doughnut_chart_data.push(
                                {
                                    value: $scope.service_completed,
                                    color: '#b2ffaf',
                                    highlight: '#00ff5f',
                                    label: "Completed"
                                }
                            );
                        }

                    });

                });

            });

            // Chart.js Options
            $scope.work_polar_chart_options = {

                // Sets the chart to be responsive
                responsive: true,

                //Boolean - Show a backdrop to the scale label
                scaleShowLabelBackdrop: true,

                //String - The colour of the label backdrop
                scaleBackdropColor: 'rgba(255,255,255,0.75)',

                // Boolean - Whether the scale should begin at zero
                scaleBeginAtZero: true,

                //Number - The backdrop padding above & below the label in pixels
                scaleBackdropPaddingY: 2,

                //Number - The backdrop padding to the side of the label in pixels
                scaleBackdropPaddingX: 2,

                //Boolean - Show line for each value in the scale
                scaleShowLine: true,

                //Boolean - Stroke a line around each segment in the chart
                segmentShowStroke: true,

                //String - The colour of the stroke on each segement.
                segmentStrokeColor: '#fff',

                //Number - The width of the stroke value in pixels
                segmentStrokeWidth: 5,

                //Number - Amount of animation steps
                animationSteps: 100,

                //String - Animation easing effect.
                animationEasing: 'easeOutBounce',

                //Boolean - Whether to animate the rotation of the chart
                animateRotate: true,

                //Boolean - Whether to animate scaling the chart from the centre
                animateScale: false,

                //String - A legend template
                legendTemplate: '<ul class="tc-chart-js-legend"><% for (var i=0; i<segments.length; i++){%><li><span style="background-color:<%=segments[i].fillColor%>"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>'
            };

            // Chart.js Options
            $scope.work_doughnut_chart_options = {

                // Sets the chart to be responsive
                responsive: true,

                //Boolean - Whether we should show a stroke on each segment
                segmentShowStroke: true,

                //String - The colour of each segment stroke
                segmentStrokeColor: '#ffffff',

                //Number - The width of each segment stroke
                segmentStrokeWidth: 5,

                //Number - The percentage of the chart that we cut out of the middle
                percentageInnerCutout: 65, // This is 0 for Pie charts

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