import logging
from datetime import datetime
from typing import Any

from django.conf import settings

from pdpyras import PDClientError
from response.core.models import ExternalUser, Incident
from response.slack.client import channel_reference
from response.slack.decorators import dialog_handler
from response.slack.settings import INCIDENT_EDIT_DIALOG, INCIDENT_REPORT_DIALOG

logger = logging.getLogger(__name__)


@dialog_handler(INCIDENT_REPORT_DIALOG)
def report_incident(
    user_id: str, channel_id: str, submission: Any, response_url: str, state: Any
):
    report = submission["report"]
    summary = submission["summary"]
    impact = submission["impact"]
    # lead_id = submission["lead"]
    severity = submission["severity"]
    pdschedule = submission["pdschedule"]

    name = settings.SLACK_CLIENT.get_user_profile(user_id)["name"]
    reporter, _ = ExternalUser.objects.get_or_create_slack(
        external_id=user_id, display_name=name
    )

    lead = None
    # if lead_id:
    # lead_name = settings.SLACK_CLIENT.get_user_profile(lead_id)["name"]
    # lead, _ = ExternalUser.objects.get_or_create_slack(
    # external_id=lead_id, display_name=lead_name
    # )

    Incident.objects.create_incident(
        report=report,
        reporter=reporter,
        report_time=datetime.now(),
        summary=summary,
        impact=impact,
        lead=lead,
        severity=severity,
    )

    try:
        if pdschedule == "yes":
            res = settings.PDSESSION.rpost(
                "/incidents",
                json={
                    "incident": {
                        "type": "incident",
                        "title": report,
                        "service": {"id": "P703RRY", "type": "service_reference"},
                        "body": {
                            "type": "incident_body",
                            "details": summary if summary else "",
                        },
                    }
                },
                headers={"From": "marcos@zeit.co"},
            )

    except PDClientError as pce:
        logger.error(pce.response.json())

    incidents_channel_ref = channel_reference(settings.INCIDENT_CHANNEL_ID)
    text = f"Thanks for raising the incident 🙏\n\nHead over to {incidents_channel_ref} to complete the report and/or help deal with the issue"
    settings.SLACK_CLIENT.send_ephemeral_message(channel_id, user_id, text)


@dialog_handler(INCIDENT_EDIT_DIALOG)
def edit_incident(
    user_id: str, channel_id: str, submission: Any, response_url: str, state: Any
):
    report = submission["report"]
    summary = submission["summary"]
    impact = submission["impact"]
    # lead_id = submission["lead"]
    severity = submission["severity"]

    lead = None
    # if lead_id:
    # lead_name = settings.SLACK_CLIENT.get_user_profile(lead_id)["name"]
    # lead, _ = ExternalUser.objects.get_or_create_slack(
    # external_id=lead_id, display_name=lead_name
    # )

    try:
        incident = Incident.objects.get(pk=state)

        # deliberately update in this way the post_save signal gets sent
        # (required for the headline post to auto update)
        incident.report = report
        incident.summary = summary
        incident.impact = impact
        incident.lead = lead
        incident.severity = severity
        incident.save()

    except Incident.DoesNotExist:
        logger.error(f"No incident found for pk {state}")
