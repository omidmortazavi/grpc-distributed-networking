import base64
import grpc
import logging
import pickle
import service_pb2
import service_pb2_grpc

from rich.logging import RichHandler


logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s"
)

logger = logging.getLogger("client_log")
logger.addHandler(logging.FileHandler("client.log"))
logger.addHandler(RichHandler())


class GRPCClient:
    def echo_test(self, stub):
        """Performs the EchoTest using the PrintMethod gRPC service.

        Args:
            stub (AutomationServiceStub): The gRPC stub object.
        """
        # Make a request to the server
        request = service_pb2.ClientRequest(data="Hello World!")
        response = stub.print_method(request)

        # Print the response received from the server
        logger.info(f"Response from server: {response.result}")

    def serialize_object(self, stub):
        """Performs the SerializeObject test using the PassObject gRPC service.

        Args:
            stub (AutomationServiceStub): The gRPC stub object.
        """
        # Client object to be sent
        client_object = {"foo": "bar"}

        # Serialize the object
        serialized_object = pickle.dumps(client_object)

        # Convert the byte string to base64-encoded string
        encoded_object = base64.b64encode(serialized_object).decode("utf-8")

        # Make a request to the server
        request = service_pb2.ClientRequest(data=encoded_object)
        response = stub.pass_object(request)

        # Print the response received from the server
        logger.info("Response from server: {}".format(response.result))

    def get_running_config(self, stub):
        """Performs the GetRunningConfig test using the GetRunningConfig gRPC service.

        Args:
            stub (AutomationServiceStub): The gRPC stub object.
        """
        # Make a request to the server using the GetRunningConfig method
        request = service_pb2.DeviceParameters(
            device_type="cisco_xe", ip="100.71.34.183", username="cisco", password="cisco"
        )
        response = stub.get_running_config(request)

        # Print the response received from the server
        logger.info(f"Response from GetRunningConfig: {response.result}")

    def run(self):
        """Runs the gRPC client."""
        # Create SSL channel credentials with the ca_file argument
        channel_credentials = grpc.ssl_channel_credentials(
            root_certificates=open("certificates/ca.crt", "rb").read()
        )

        # Create a secure channel using SSL credentials
        channel = grpc.secure_channel("localhost:50051", channel_credentials)

        # Create a stub (client) using the generated service classes
        stub = service_pb2_grpc.AutomationServiceStub(channel)

        # Run Echo Test
        self.echo_test(stub)

        # Run Pickle Test
        self.serialize_object(stub)

        # Run Netmiko Test
        self.get_running_config(stub)


if __name__ == "__main__":
    client = GRPCClient()
    client.run()