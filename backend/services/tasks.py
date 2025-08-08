"""Tasks module that delegates work to gRPC services."""

from backend.schemas.lead import LeadOut
from backend.services.grpc_client import LeadServiceClient

_client = LeadServiceClient()


def send_new_lead_notification(lead: LeadOut) -> None:
    """Send a notification about a new lead via gRPC."""
    _client.send_notification(lead)


def generate_lead_pdf(lead: LeadOut) -> str:
    """Generate a lead PDF using a gRPC service."""
    return _client.generate_pdf(lead)
