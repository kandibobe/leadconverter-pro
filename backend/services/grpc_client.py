import grpc
from app.api.protos import lead_pb2, lead_pb2_grpc
from app.schemas.lead import LeadOut

class LeadServiceClient:
    """Simple gRPC client for interacting with the LeadService."""

    def __init__(self, target: str = "localhost:50051") -> None:
        self._target = target

    def _create_stub(self):
        channel = grpc.insecure_channel(self._target)
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
