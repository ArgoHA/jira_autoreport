# jira_autoreport
This python script creates jira issue and attaches a screenshot of needed dashboard.
When some rule was broken - appdynamics fire the script. Script checks what rule was broken, goes to specific dashboard, make a screenshot and open an issue on jira with attached image. Script can be configured via jira_autoreport.yml file.

Данный python скрипт создает задачу в jira и прикрепляет скрин шот нужного дашборда.
Когда в приложении appdynamic нарушенается какое-то правило, запускается скрипт, проверяет какое именно правило было нарушено, находит нудный дашборд и создает задачу в jira, после чего прикрепляет туда скрин шот дашборда. Скрипт настраивается из конфигурационнога файла jira_autoreport.yml
