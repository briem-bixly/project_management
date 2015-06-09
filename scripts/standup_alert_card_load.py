class standup_alert_card_load(NebriOS):
    listens_to = ['standup_alert_card_load']

    def check(self):
        return self.standup_alert_card_load == True

    def action(self):
        self.standup_alert_card_load = "Ran"
        # first, get the user's employee process
        user_process = Process.objects.get(user=request.user, kind="employee")
        # use that PID to get all processes for that user in a standup tree
        user_standups = Process.objects.filter(user_pid=user_process.PROCESS_ID, kind="standup_employee")
        self.standups = []
        for u in user_standups:
            if u.PARENT not in self.standups:
                self.standups.append(u.PARENT)
        load_card('standup-alert-card')
        for s in self.standups:
            p = Process.objects.create(
                standup = s['name'],
                past_day = '',
                today = '',
                roadblocks = ''
            )         
            p.save()
            load_card('standup-reminder-card', pid=p.PROCESS_ID, user=self.last_actor)
