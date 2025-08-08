import grpc
from backend.api.protos import lead_pb2, lead_pb2_grpc
from backend.schemas.lead import LeadOut
from backend.core.config import settings

class LeadServiceClient:
    """Simple gRPC client for interacting with the LeadService."""

    def __init__(self, target: str = "localhost:50051") -> None:
        self._target = target

    def _create_stub(self):
        channel = grpc.insecure_channel(self._target)
        if not settings.GRPC_CA_PATH:
            raise ValueError("GRPC_CA_PATH is not set")

        with open(settings.GRPC_CA_PATH, "rb") as f:
            root_cert = f.read()

        private_key = certificate_chain = None
        if settings.GRPC_KEY_PATH and settings.GRPC_CERT_PATH:
            with open(settings.GRPC_KEY_PATH, "rb") as f:
                private_key = f.read()
            with open(settings.GRPC_CERT_PATH, "rb") as f:
                certificate_chain = f.read()

        credentials = grpc.ssl_channel_credentials(
            root_certificates=root_cert,
            private_key=private_key,
            certificate_chain=certificate_chain,
        )
        channel = grpc.secure_channel(self._target, credentials)
        stub = lead_pb2_grpc.LeadServiceStub(channel)
        return stub, channel

    def send_notification(self, lead: LeadOut) -> None:
        stub, channel = self._create_stub()
        request = lead_pb2.LeadData(
            client_email=lead.client_email,
            final_price=lead.final_price,
        )
        stub.SendNotification(request)
        channel.close()

    def generate_pdf(self, lead: LeadOut) -> str:
        stub, channel = self._create_stub()
        request = lead_pb2.LeadData(
            client_email=lead.client_email,
            final_price=lead.final_price,
        )
        response = stub.GeneratePdf(request)
        channel.close()
        return response.path
