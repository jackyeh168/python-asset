# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple

from google.api_core import grpc_helpers_async  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.asset_v1.types import asset_service
from google.longrunning import operations_pb2 as operations  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore

from .base import AssetServiceTransport
from .grpc import AssetServiceGrpcTransport


class AssetServiceGrpcAsyncIOTransport(AssetServiceTransport):
    """gRPC AsyncIO backend transport for AssetService.

    Asset service definition.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(
        cls,
        host: str = "cloudasset.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            address (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """
        scopes = scopes or cls.AUTH_SCOPES
        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "cloudasset.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: aio.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id=None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): The mutual TLS endpoint. If
                provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]): A
                callback to provide client SSL certificate bytes and private key
                bytes, both in PEM format. It is ignored if ``api_mtls_endpoint``
                is None.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        if channel:
            # Sanity check: Ensure that channel and credentials are not both
            # provided.
            credentials = False

            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
        elif api_mtls_endpoint:
            host = (
                api_mtls_endpoint
                if ":" in api_mtls_endpoint
                else api_mtls_endpoint + ":443"
            )

            # Create SSL credentials with client_cert_source or application
            # default SSL credentials.
            if client_cert_source:
                cert, key = client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
            else:
                ssl_credentials = SslCredentials().ssl_credentials

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                credentials_file=credentials_file,
                ssl_credentials=ssl_credentials,
                scopes=scopes or self.AUTH_SCOPES,
                quota_project_id=quota_project_id,
            )

        # Run the base constructor.
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes or self.AUTH_SCOPES,
            quota_project_id=quota_project_id,
        )

        self._stubs = {}

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Sanity check: Only create a new channel if we do not already
        # have one.
        if not hasattr(self, "_grpc_channel"):
            self._grpc_channel = self.create_channel(
                self._host, credentials=self._credentials,
            )

        # Return the channel from cache.
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsAsyncClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Sanity check: Only create a new client if we do not already have one.
        if "operations_client" not in self.__dict__:
            self.__dict__["operations_client"] = operations_v1.OperationsAsyncClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self.__dict__["operations_client"]

    @property
    def export_assets(
        self,
    ) -> Callable[[asset_service.ExportAssetsRequest], Awaitable[operations.Operation]]:
        r"""Return a callable for the export assets method over gRPC.

        Exports assets with time and resource types to a given Cloud
        Storage location/BigQuery table. For Cloud Storage location
        destinations, the output format is newline-delimited JSON. Each
        line represents a
        [google.cloud.asset.v1.Asset][google.cloud.asset.v1.Asset] in
        the JSON format; for BigQuery table destinations, the output
        table stores the fields in asset proto as columns. This API
        implements the
        [google.longrunning.Operation][google.longrunning.Operation] API
        , which allows you to keep track of the export. We recommend
        intervals of at least 2 seconds with exponential retry to poll
        the export operation result. For regular-size resource parent,
        the export operation usually finishes within 5 minutes.

        Returns:
            Callable[[~.ExportAssetsRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "export_assets" not in self._stubs:
            self._stubs["export_assets"] = self.grpc_channel.unary_unary(
                "/google.cloud.asset.v1.AssetService/ExportAssets",
                request_serializer=asset_service.ExportAssetsRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["export_assets"]

    @property
    def batch_get_assets_history(
        self,
    ) -> Callable[
        [asset_service.BatchGetAssetsHistoryRequest],
        Awaitable[asset_service.BatchGetAssetsHistoryResponse],
    ]:
        r"""Return a callable for the batch get assets history method over gRPC.

        Batch gets the update history of assets that overlap a time
        window. For IAM_POLICY content, this API outputs history when
        the asset and its attached IAM POLICY both exist. This can
        create gaps in the output history. Otherwise, this API outputs
        history with asset in both non-delete or deleted status. If a
        specified asset does not exist, this API returns an
        INVALID_ARGUMENT error.

        Returns:
            Callable[[~.BatchGetAssetsHistoryRequest],
                    Awaitable[~.BatchGetAssetsHistoryResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_get_assets_history" not in self._stubs:
            self._stubs["batch_get_assets_history"] = self.grpc_channel.unary_unary(
                "/google.cloud.asset.v1.AssetService/BatchGetAssetsHistory",
                request_serializer=asset_service.BatchGetAssetsHistoryRequest.serialize,
                response_deserializer=asset_service.BatchGetAssetsHistoryResponse.deserialize,
            )
        return self._stubs["batch_get_assets_history"]

    @property
    def create_feed(
        self,
    ) -> Callable[[asset_service.CreateFeedRequest], Awaitable[asset_service.Feed]]:
        r"""Return a callable for the create feed method over gRPC.

        Creates a feed in a parent
        project/folder/organization to listen to its asset
        updates.

        Returns:
            Callable[[~.CreateFeedRequest],
                    Awaitable[~.Feed]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_feed" not in self._stubs:
            self._stubs["create_feed"] = self.grpc_channel.unary_unary(
                "/google.cloud.asset.v1.AssetService/CreateFeed",
                request_serializer=asset_service.CreateFeedRequest.serialize,
                response_deserializer=asset_service.Feed.deserialize,
            )
        return self._stubs["create_feed"]

    @property
    def get_feed(
        self,
    ) -> Callable[[asset_service.GetFeedRequest], Awaitable[asset_service.Feed]]:
        r"""Return a callable for the get feed method over gRPC.

        Gets details about an asset feed.

        Returns:
            Callable[[~.GetFeedRequest],
                    Awaitable[~.Feed]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_feed" not in self._stubs:
            self._stubs["get_feed"] = self.grpc_channel.unary_unary(
                "/google.cloud.asset.v1.AssetService/GetFeed",
                request_serializer=asset_service.GetFeedRequest.serialize,
                response_deserializer=asset_service.Feed.deserialize,
            )
        return self._stubs["get_feed"]

    @property
    def list_feeds(
        self,
    ) -> Callable[
        [asset_service.ListFeedsRequest], Awaitable[asset_service.ListFeedsResponse]
    ]:
        r"""Return a callable for the list feeds method over gRPC.

        Lists all asset feeds in a parent
        project/folder/organization.

        Returns:
            Callable[[~.ListFeedsRequest],
                    Awaitable[~.ListFeedsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_feeds" not in self._stubs:
            self._stubs["list_feeds"] = self.grpc_channel.unary_unary(
                "/google.cloud.asset.v1.AssetService/ListFeeds",
                request_serializer=asset_service.ListFeedsRequest.serialize,
                response_deserializer=asset_service.ListFeedsResponse.deserialize,
            )
        return self._stubs["list_feeds"]

    @property
    def update_feed(
        self,
    ) -> Callable[[asset_service.UpdateFeedRequest], Awaitable[asset_service.Feed]]:
        r"""Return a callable for the update feed method over gRPC.

        Updates an asset feed configuration.

        Returns:
            Callable[[~.UpdateFeedRequest],
                    Awaitable[~.Feed]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_feed" not in self._stubs:
            self._stubs["update_feed"] = self.grpc_channel.unary_unary(
                "/google.cloud.asset.v1.AssetService/UpdateFeed",
                request_serializer=asset_service.UpdateFeedRequest.serialize,
                response_deserializer=asset_service.Feed.deserialize,
            )
        return self._stubs["update_feed"]

    @property
    def delete_feed(
        self,
    ) -> Callable[[asset_service.DeleteFeedRequest], Awaitable[empty.Empty]]:
        r"""Return a callable for the delete feed method over gRPC.

        Deletes an asset feed.

        Returns:
            Callable[[~.DeleteFeedRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_feed" not in self._stubs:
            self._stubs["delete_feed"] = self.grpc_channel.unary_unary(
                "/google.cloud.asset.v1.AssetService/DeleteFeed",
                request_serializer=asset_service.DeleteFeedRequest.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_feed"]

    @property
    def search_all_resources(
        self,
    ) -> Callable[
        [asset_service.SearchAllResourcesRequest],
        Awaitable[asset_service.SearchAllResourcesResponse],
    ]:
        r"""Return a callable for the search all resources method over gRPC.

        Searches all the resources within the given
        accessible scope (e.g., a project, a folder or an
        organization). Callers should have
        cloud.assets.SearchAllResources permission upon the
        requested scope, otherwise the request will be rejected.

        Returns:
            Callable[[~.SearchAllResourcesRequest],
                    Awaitable[~.SearchAllResourcesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "search_all_resources" not in self._stubs:
            self._stubs["search_all_resources"] = self.grpc_channel.unary_unary(
                "/google.cloud.asset.v1.AssetService/SearchAllResources",
                request_serializer=asset_service.SearchAllResourcesRequest.serialize,
                response_deserializer=asset_service.SearchAllResourcesResponse.deserialize,
            )
        return self._stubs["search_all_resources"]

    @property
    def search_all_iam_policies(
        self,
    ) -> Callable[
        [asset_service.SearchAllIamPoliciesRequest],
        Awaitable[asset_service.SearchAllIamPoliciesResponse],
    ]:
        r"""Return a callable for the search all iam policies method over gRPC.

        Searches all the IAM policies within the given
        accessible scope (e.g., a project, a folder or an
        organization). Callers should have
        cloud.assets.SearchAllIamPolicies permission upon the
        requested scope, otherwise the request will be rejected.

        Returns:
            Callable[[~.SearchAllIamPoliciesRequest],
                    Awaitable[~.SearchAllIamPoliciesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "search_all_iam_policies" not in self._stubs:
            self._stubs["search_all_iam_policies"] = self.grpc_channel.unary_unary(
                "/google.cloud.asset.v1.AssetService/SearchAllIamPolicies",
                request_serializer=asset_service.SearchAllIamPoliciesRequest.serialize,
                response_deserializer=asset_service.SearchAllIamPoliciesResponse.deserialize,
            )
        return self._stubs["search_all_iam_policies"]


__all__ = ("AssetServiceGrpcAsyncIOTransport",)
