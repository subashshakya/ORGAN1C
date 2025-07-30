from channels.generic.websocket import AsyncWebsocketConsumer
import json

from config.enums import PostUpdateType


class PostConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.post_id = self.scope["url_route"]["kwargs"]["post_id"]
        self.group_name = f"post_{self.post_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.close(code=6699)

    async def post_update(self, event):
        response_data = {"post_id": event["post_id"]}
        match event["from"]:
            case PostUpdateType.LIKED:
                response_data["likes_count"] = event["likes_count"]
            case PostUpdateType.COMMENTED:
                response_data["comments_count"] = event["comments_count"]
            case PostUpdateType.SHARED:
                response_data["shares_count"] = event["shares_count"]
        await self.send(text_data=json.dumps(response_data))
