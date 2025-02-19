from jira import JIRA

from .config import settings 

jira = JIRA(settings.JIRA.JIRA_URL, token_auth=settings.JIRA.JIRA_TOKEN)