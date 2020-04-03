import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import analysis
from my_token import TOKEN


def main():
    vk_session = vk_api.VkApi(
        token=TOKEN)

    longpoll = VkBotLongPoll(vk_session, '193289108')

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            #print(event)
            #print('Новое сообщение:')
            #print('Для меня от:', event.obj.message['from_id'])
            #print('Текст:', event.obj.message['text'])
            vk = vk_session.get_api()
            #print(event.obj.client_info)
            message = analysis.Analysis(event.obj.message['text']).get_result()
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=message,
                             random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
