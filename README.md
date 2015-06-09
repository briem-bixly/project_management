# project_management
Project Management App for NebriOS

This app is intended for use in a NebriOS instance. Visit https://nebrios.com to sign up for free!

NOTE This app has dependencies in https://github.com/briem-bixly/organization_management and https://github.com/briem-bixly/human_resources

<h4>Setup</h4>
This app requires very little in terms of setup. Please ensure that all files are placed in the correct places over SFTP.
  - project_info_card_load.py and standup_alert_card_load.py should be copied to /scripts
  - project_management.py should be copied to /api
  - project-info-card.html, standup-alert-card.html, and standup-reminder-card.html should be copied to /card_html_files

<h4>Creating/Updating Projects</h4>
  - running project_info_card_load from debug mode will trigger a card in interact mode

    ```
    project_info_card_load := True
    ```
  - without any additional arguments, this will load a blank card and allow you to create a new project
  - in order to update an existing project, the name argument can be sent as well

    ```
    project_info_card_load := True
    name := "Example Project"
    ```
  - this will pre fill the project info card with the currently set info for that project
