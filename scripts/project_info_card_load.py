from api.human_resources import get_pms, get_developers
from api.project_management import find_project

import logging

logging.basicConfig(filename="project_management.log", level=logging.DEBUG)

class project_info_card_load(NebriOS):
    listens_to = ['project_info_card_load']

    def check(self):
        return self.project_info_card_load == True

    def action(self):
        self.project_info_card_load = "Ran"
        self.pms = [{'value': pm['email'], 'label': '%s %s' %(pm['first_name'], pm['last_name'])} for pm in get_pms(self)]
        logging.debug(self.pms)
        self.devs = [{'value': dev['email'], 'label': '%s %s' %(dev['first_name'], dev['last_name'])} for dev in get_developers(self)]
        target_project = find_project(self)
        self.valid_days = [{'value': 'Monday', 'label': 'Monday'},
        {'value': 'Tuesday', 'label': 'Tuesday'},
        {'value': 'Wednesday', 'label': 'Wednesday'},
        {'value': 'Thursday', 'label': 'Thursday'},
        {'value': 'Friday', 'label': 'Friday'}]
        self.editing = False
        if target_project is not None:
            self.editing = True
            self.name = target_project['name']
            self.description = target_project['description']
            self.client_name = target_project['client_name']
            self.standup_days = target_project['standup_days']
            self.standup_time = target_project['standup_time']
            self.is_active = target_project['is_active']
            self.developers = target_project['developers']
        load_card('project-info-card')

