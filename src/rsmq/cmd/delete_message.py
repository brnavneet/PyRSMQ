'''

'''

from .base_command import BaseRSMQCommand


class DeleteMessageCommand(BaseRSMQCommand):
    '''
    Delete Message if it exists
    '''

    PARAMS = {'qname': {'required': True,
                        'value': None},
              'id': {'required': True,
                     'value': None}
              }

    def exec_command(self):
        ''' Exec Command '''
        client = self.client
        queue_base = self.queue_base
        queue_key = self.queue_key
        message_id = self.get_id

        tx = client.pipeline(transaction=True)
        tx.zrem(queue_base, message_id)
        tx.hdel(queue_key, message_id, "%s:rc" %
                message_id, "%s:fr" % message_id)
        result = tx.execute()

        self.log.debug("Result: %s", result)
        if int(result[0]) == 1 and int(result[1]) > 0:
            return True

        return False
