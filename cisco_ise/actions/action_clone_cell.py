from lib.base import BaseAction


class EgressMatrixCellAction(BaseAction):
    def run(self, **kwargs):

        cell_id = kwargs.pop('cell_id', None)
        source_sgt_id = kwargs.pop('source_sgt_id', None)
        dest_sgt_id = kwargs.pop('destination_sgt_id', None)

        if not cell_id or not source_sgt_id or not dest_sgt_id:
            self.logger.debug(f'cell_id value was: {cell_id}')
            self.logger.debug(f'source_sgt_id value was: {source_sgt_id}')
            self.logger.debug(f'destination_sgt_id value was: {dest_sgt_id}')
            raise ValueError('A required field is missing')

        kwargs['resource_id'] = f'{cell_id}/srcSgt/{source_sgt_id}/dstSgt/{dest_sgt_id}'

        # Call multiple methods that parse and prepare data
        # and creates objects that can be used to call api_request()
        self.action_setup(**kwargs)

        return self.api_client(
            http_method=self.http_method,
            request_uri=self.request_uri,
            api_user=self.connection['api_user'],
            api_pass=self.connection['api_pass'],
            verify_ssl=self.connection['verify_ssl'],
            payload=self.payload)
