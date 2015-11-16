# Gallant Calendar Documentation

**API Documentation**

Gallant Calendar is a fully functional task management calendar based on Fullcalendar https://github.com/fullcalendar/fullcalendar-scheduler and Angular-ui-calendar https://github.com/angular-ui/ui-calendar

**Required Scripts**

- calendr/Calendr_3.html
- calendr/app.js
- calendr/services.js
- calendr/controllers.js
- calendr/directives.js
- ui-calendar/calendar.js
- fullcalendar-ng/scheduler.js
- fullcalendar-ng/Fullcalendar.min.js
- fullcalendar-ng/moment.min.js
- angular.min.js
- angular-aside.min.js
- angular-resource.min.js
- ui-bootstrap-tpls-0.14.0.js


**Watched arrays**

Watched arrays are watched by angularjs.watch method, in case of any change (eg. Push or Remove) they will be re-rendered on the calendar.

    events = [];  
    eventResources = [];  

>Watchers are located in calendar.js

**Modals**

	Name:           editTaskModal		
	File:           alendar_modal.html
	Decription:     Modal used to edit task attributes
	
	Method:         asideModal		
	File:           aside.html
	Description:    Sidebar used to display user tasks.

**Relevant Controller Methods**

***Get Resources***

    Method:         getResources( [project] )
    Description:    Calls User resource, might optionally receive a Project object as parameter in order to receive only users that belong to the selected project.

>This method is called every time the calendar project is changed.

***Get Tasks***

    Method:         getTasks()
    Description:    Calls Task resource and returns all Tasks.

***Get Projects***

    Method:         getProjects()
    Description:    Calls Project resource and returns all User Projects. If user is superuser returns all projects.


***Render event***

    Method:         renderEvent(event)
    Description:    Method used to render an event in the calendar

***Project Changed***

    Method:         projectChanged( [project] )
    Description:    Receives a project as a parameter and renders all users for that project.
    
***Go to Date***

    Method:         gotoDate( date )
    Description:    Takes the calendar to the specified date
    
***Open Aside Modal***

    Method:         openAsideModal()
    Description:    Open sidebar modal

***Open Edit Modal***


    Method:         openEditModal(event) 
    Description:    Open edit modal for the given event

***Select Function (Drag and create)***


    Method:         selectFunction( start, end , x , y, resource)
    Description:    Receives the selected start and end date in the calendar and calls openEditModal(event) to create a new event.

**Resources**

	Resource:      Task
	Url:             /en/calendar/api/task
	Methods:      
            		* query (GET)
            		* save (POST) 
            		* update (PUT)
	Description:    Fetch all tasks.


    Resource:       User
    Url:            /en/api/users
    Description:    Fetch all users for the given Project.

    Resource:       Project
    Url:            /en/api/projects
    Description:    Fetch all projects
