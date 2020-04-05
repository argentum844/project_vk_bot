import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.upload import VkUpload
import random
import analysis
from my_token import TOKEN


def main():
    vk_session = vk_api.VkApi(
        token=TOKEN)

    longpoll = VkBotLongPoll(vk_session, '193289108')

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            upload = VkUpload(vk)
            message = analysis.Analysis(event.obj.message['text']).get_result()
            if type(message) != str:
                response = upload.photo_messages(message)[0]
                owner_id = response['owner_id']
                photo_id = response['id']
                access_key = response['access_key']
                attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                vk.messages.send(user_id=event.obj.message['from_id'],
                                attachment=attachment,
                                random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=message,
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
