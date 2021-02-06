from bs4 import BeautifulSoup
import requests
import vk_api
import time
import sys

f1 = open(r'D:\\TEST FILES\\THESIS\\Корпус до обработки в RStudio\\new_ids.txt', 'r', encoding='utf8')
ids=[]
for line in f1:
    k = line.replace('\n','')
    ids.append(k)

f1.close()

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """

    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    #  Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)

def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция.
    """

    #  Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    #  Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def main():
    """ Пример обработки двухфакторной аутентификации """

    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(
        login, password,
        # функция для обработки двухфакторной аутентификации
        auth_handler=auth_handler,
        captcha_handler=captcha_handler
    )

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()


    for user in ids:
        f = open(r'D:\TEST FILES\THESIS\Корпус до обработки\new\VK_PARSING_'+str(user)+'.txt', 'w', encoding = 'utf-8')

        response = vk.wall.get(owner_id = str(user), count=200)  #  Используем метод wall.get

        print('Пользователь '+user+'\n\n')
        print('Пользователь '+user+'\n\n', file=f)

        for k in response['items']:  # для списка постов с разными значениями
            if len(k['text'].translate(non_bmp_map)):
                if 'copy_history' in k:
                    text = k['copy_history'][0]
                    check_len = len(text['text'].translate(non_bmp_map) + k['text'].translate(non_bmp_map))  # Длина поста и репоста вместе
                    if '2014' not in str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(k['date']))) and '2017' not in str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(k['date']))) and '2016' not in str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(k['date']))) and '2015' not in str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(k['date']))) and check_len > 200:
                        print(k['text'].translate(non_bmp_map))
                        print(text['text'].translate(non_bmp_map))  # текст репоста
                        print(k['text'].translate(non_bmp_map), file=f)
                        print(text['text'].translate(non_bmp_map), file=f)  # текст репоста
                        tme = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(k['date']))  # перевод от количества секунд с начала времён (например, 1999929929299292) в нормальное время
                        print('Дата создания поста - ', tme)
                        print('----------------------------------------------------------\n')
                        print('Дата создания поста - ', tme, file=f)
                        print('----------------------------------------------------------\n', file=f)
                else:
                    if len(k['text'].translate(non_bmp_map)) > 200 and '2014' not in str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(k['date']))) and '2017' not in str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(k['date']))) and '2016' not in str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(k['date']))) and '2015'not in str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(k['date']))):
                        print(k['text'].translate(non_bmp_map))
                        print(k['text'].translate(non_bmp_map), file=f)
                        tme = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(k['date']))  # перевод от количества секунд с начала времён (например, 1999929929299292) в нормальное время
                        print('Дата создания поста - ', tme)
                        print('----------------------------------------------------------\n')
                        print('Дата создания поста - ', tme, file=f)
                        print('----------------------------------------------------------\n', file=f)

        f.close()

if __name__ == '__main__':
    main()


