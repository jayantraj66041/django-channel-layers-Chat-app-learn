from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("Websocket Connected...", event)
        print("Channel layer -", self.channel_layer)    # get default channel layer
        print("Channel name -", self.channel_name)    # get default channel name

        # add channel in a group name 'programmer'
        async_to_sync(self.channel_layer.group_add)(      # for converting funct. from async to sync
            "programmers",          # group name
            self.channel_name       # channel name
        )
        self.send({
            'type': 'websocket.accept'
        })
    
    def websocket_receive(self, event):
        # print("Websocket Received....", event['text'])
        print("Websocket Received type....", type(event['text']))
        async_to_sync(self.channel_layer.group_send)(
            'programmers',
            {
                'type': 'chat.msg',
                'message': event['text']
            }
        )
    
    def chat_msg(self, event):
        print("EVENT -", event)
        print("Actual data -", event['message'])
        self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

    def websocket_disconnect(self, event):
        print("Websocket Disconnected...", event)
        print("Channel layer -", self.channel_layer)    # get default channel layer
        print("Channel name -", self.channel_name)    # get default channel name

        async_to_sync(self.channel_layer.group_discard)(
            'programmers',
            self.channel_name
        )
        raise StopConsumer()

class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Websocket Connected...", event)
        print("Channel layer -", self.channel_layer)    # get default channel layer
        print("Channel name -", self.channel_name)    # get default channel name

        # add channel in a group name 'programmer'
        await self.channel_layer.group_add(      # for converting funct. from async to sync
            "programmers",          # group name
            self.channel_name       # channel name
        )
        await self.send({
            'type': 'websocket.accept'
        })
    
    async def websocket_receive(self, event):
        # print("Websocket Received....", event['text'])
        print("Websocket Received type....", type(event['text']))
        await self.channel_layer.group_send(
            'programmers',
            {
                'type': 'chat.msg',
                'message': event['text']
            }
        )
    
    async def chat_msg(self, event):
        print("EVENT -", event)
        print("Actual data -", event['message'])
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

    async def websocket_disconnect(self, event):
        print("Websocket Disconnected...", event)
        print("Channel layer -", self.channel_layer)    # get default channel layer
        print("Channel name -", self.channel_name)    # get default channel name

        await self.channel_layer.group_discard(
            'programmers',
            self.channel_name
        )
        raise StopConsumer()