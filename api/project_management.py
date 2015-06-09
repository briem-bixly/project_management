# API for project management functionality
import logging

logging.basicConfig(filename='project_management.log', level=logging.DEBUG)

valid_project_kvps = ['name', 'project_pm', 'developers', 'client_name', 'description', 'standup_days', 'standup_time', 'is_active']

def update_standup(request):
    if not isinstance(request, Process) and not isinstance(request, NebriOS):
        if request.FORM is not None:
            logging.debug(request.PROCESS)
            logging.debug(request.FORM)
            data = request.FORM
        else:
            # if using this via requests, please remember to send a PROCESS_ID and last_actor
            logging.debug(request.BODY)
            data = request.BODY
    else:
        logging.debug(request)
        data = request
    # now we have data from the form, get the user associated
    user_process = Process.objects.get(email=data.last_actor, kind="employee")
    # now let's get the standup_employee
    standup_user = Process.objects.get(user_pid=user_process.PROCESS_ID, kind="standup_employee")  # need to add filtering on the date as well
    standup_user.past_day = data.past_day
    standup_user.today = data.today
    standup_user.roadblocks = data.roadblocks
    standup_user.save()
    
    
def find_project(request):
    if not isinstance(request, Process) and not isinstance(request, NebriOS):
        if request.FORM is None:
            project_name = request.BODY['project_name']
        else:
            project_name = request.FORM['project_name']
    else:
        project_name = request.name
    try:
        project = Process.objects.get(kind="project", is_active=True, name=project_name)
        return project
    except:
        return None
    
    
def update_project(request):
    if not isinstance(request, Process) and not isinstance(request, NebriOS):
        if request.FORM is not None:
            data = request.FORM
        else:
            data = request.BODY
    else:
        data = request
    # first, let's see if this is a new project or update
    try:
        project = Process.objects.get(kind="project", name=data['name'])
        for key, value in data:
            if key not in valid_project_kvps:
                continue
            project[key] = value
        project.save()
    except:
        # need to create a new project.
        project = Process.objects.create(kind="project", is_active=True)
        for key, value in data:
            if key not in valid_project_kvps:
                continue
            project[key] = value
        project.save()
    
    
def send_standup_info(request):
    email_body = ""
    if not isinstance(request, Process) and not isinstance(request, NebriOS):
        if request.FORM is not None:
            data = request.FORM
        else:
            data = request.BODY
    else:
        data = request
    pm_process = Process.objects.get(PROCESS_ID=data.project_pm)
    standup_employees = data.CHILDREN
    to_append = "<h2>Stand Up Information For %s</h2>\n" % data.project_name
    for emp in standup_employees:
        user_process = Process.objects.get(PROCESS_ID=emp.user_pid)
        to_append += "<h4>%s</h4>\n" % user_process.name
        to_append += "<ol><li>%s</li>" % emp.past_day
        to_append += "<li>%s</li>" % emp.today
        to_append += "<li>%s</li></ol>" % emp.roadblocks
    email_body += to_append
    if email_body != '':
        send_email(pm_process.email, email_body)
    else:
        logger.debug("No Stand Ups for %s" % data.project_name)
        
        
def check_standup_completeness(request):
    if not isinstance(request, Process) and not isinstance(request, NebriOS):
        if request.FORM is not None:
            data = request.FORM
        else:
            data = request.BODY
    else:
        data = request
    standup_employees = data.CHILDREN
    ready = True
    need_standups = []
    for emp in standup_employees:
        if emp.past_day == "" or emp.today == "":
            ready = False
            need_standups.append(emp)
    return ready, need_standups
