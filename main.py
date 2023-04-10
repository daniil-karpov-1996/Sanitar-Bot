# Импортируем необходимые библиотеки.
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
import requests
import os
import datetime
import time
import os.path
import sqlite3
from random import choice

city = ""
stage = 0
check_started = 0
answer = [0, 0, 0]
advices = [["Принимайте холодный душ", "Холодный душ раз в день  улучшает кровообращение, ускоряет обмен веществ,"
                                       " сужает поры, повышает иммунитет и помогает восстановиться после "
                                       "интенсивных физических упражнений."],
           [" Попробуйте разгрузочные дни", "Краткосрочное голодание избавляет организм от токсинов, помогает"
                                            " похудеть и даже замедляет старение ."],
           ["Ешьте, не отвлекаясь", "Первый шаг к осознанному питанию - это убрать все то, что отвлекает вас во время"
                                    " еды. Отключите телевизор, отложите телефон и уделите максимум внимания тому, что"
                                    " вы едите."],
           ["Дышите животом", "Лягте на спину, закройте глаза, подумайте о чем-то хорошем и попробуйте дышать животом."
                              " Вы можете положить какой-то предмет – книгу или небольшие гантели на живот, чтобы лучше"
                              " прочувствовать это дыхание."],
           ["Чистите зубы кокосовым маслом", "Кокосовое масло стало очень популярным благодаря целому ряду своих"
                                             " полезных свойств. Кроме прекрасных свойств увлажнения и смягчения,"
                                             " кокосовое масло можно использовать и в качестве зубной пасты либо в "
                                             "чистом виде, либо в смеси с пищевой содой ."],
           ["Ешьте черный шоколад", "Исследования показали, что ежедневное потребление"
                                    " 45 грамм черного шоколада полезно для сердца, мозга и в целом для здоровья."],
           ["Меняйте положение тела", "Меняйте положение тела каждые 20 минут . Встаньте, постойте на одной ноге,"
                                      " сядьте на стул, сядьте на пол, скрестив ноги, а затем выпрямив их, сядьте "
                                      "на колени, на ступни, встаньте и потянитесь. "],
           ["Здоровое питание", "Заведите себе привычку есть всегда в одно и то же время"],
           ["Здоровое питание", "Не ешьте поздно вечером перед сном и посреди ночи"],
           ["Здоровое питание", "Замените сладкие фруктовые и овощные соки самими фруктами и овощами"],
           ["Здоровое питание", "Сведите свое потребление сахара и сладкой пищи к минимуму. Сахар — это 100% простой"
                                " углевод (самый вредный)"],
           ["Здоровое питание", "Не злоупотребляйте солью. Это очень важно. Чрезмерное потребление соли косвенная"
                                " причина более чем 100 000 смертей в России ежегодно"],
           ["Здоровое питание", "Если Вы пьете воду из под крана, то хотя бы пропускайте ее через фильтр и обязательно "
                                "кипятите. И пропускайте воду по утрам. В это время в ней много вредных микроорганизмов"
                                " которые расплодились в стоячей воде за ночь;"],
           ["Здоровый сон", "Ложитесь и вставайте каждый день в одно и то же время. Даже по выходным. Желательно"
                            " максимально близко совместить график сна с заходом солнца"],
           ["Здоровый сон", "Не пренебрегайте но и не злоупотребляйте сном. Оптимально 7-8 часов сна в сутки"],
           ["Здоровый сон", " Откройте на ночь форточку. Главное, что бы не было сквозняка. Оптимальная"
                            " температура для хорошего сна 18 °C. И не пытайтесь заменить свежий воздух с улицы"
                            " воздухом из кондиционера. Кондиционер не берет воздух с улицы а просто охлаждает тот,"
                            " что уже есть в комнате;"],
           ["Здоровый сон",
            "Не спите на слишком мягких кроватях и диванах. Даже если сейчас все в порядке, то в будущем"
            " Ваша спина не будет Вам за это благодарна"],
           ["Зрение", " Если ваша работа или отдых связанны с напряжением на Ваши органы зрения то делайте перерыв"
                      " раз в час на 10 минут. (Оторвитесь хотя бы не на долго от компьютера, телевизора или книги);"],
           ["Зрение", "Ягоды черники снизят утомляемость глаз если Вы часто сталкиваетесь с данной проблемой;"],
           ["Зрение", "Старайтесь ничего не делать в темноте и полумраке. Объяснять почему думаем будет излишним"],
           ["Зрение", "Обратите внимание на освещение в вашей квартире и на рабочем месте. Возможно стоит купить"
                      " лампочки по мощнее или купить дополнительную настольную лампу."],
           ["Слух", "Не слушайте музыку в наушниках. Если все же Вам это доставляет сказочное удовольствие то не"
                    " делайте этого слишком долго и не выкручивайте громкость на полную."],
           ["Сердечно-сосудистая система", "Откажитесь от курения. О его вреде знают все, но почему-то находят"
                                           " оправдания для наличия у себя этой пагубной привычки. А их нет и быть"
                                           " не может."],
           ["Сердечно-сосудистая система", "Сведите в минимуму потребление алкоголя. Если только это не 100 мг. вина"
                                           " за обедом или ужином, или не семейный праздник. "],
           ["Сердечно-сосудистая система", "Возьмите за привычку небольшие пробежки трусцой в теплое время года. "],
           ["Сердечно-сосудистая система", "Постарайтесь как можно меньше нервничать или переживать по пустякам."],
           ["Здоровые нервы и психика", "Улыбайтесь и смейтесь как можно чаще! Польза хорошего настроения для здоровья"
                                        " — это не миф"],
           ["Здоровые нервы и психика", " Ограничьте контакты с людьми которые вызывают у Вас депрессию своими советами"
                                        " как Вам надо жить, что делать, мнением о том почему Вы не правы и пр."],
           ["Здоровые нервы и психика", " Не обращайте внимания на свой возраст и не обращайте внимание на тех кто"
                                        " делает это за Вас. Если Вы хотите чего-то делайте. Хотите получить"
                                        " образование — дерзайте. Хотите научиться кататься на велосипеде — валяйте."
                                        " Не существует вещей для которых слишком поздно;"],
           ["Здоровые нервы и психика", "Заводите новые знакомства и общайтесь с людьми. Но делайте это в тех пределах"
                                        " в которых Вам это комфортно (не всем же, в самом деле, быть экстравертами);"],
           ["Мозг", "Изучайте иностранный язык. Сколько бы лет Вам не было. Хороший сон и такая хорошая нагрузка на"
                    " мозг как изучение незнакомого Вам языка — это самые лучшие способы для профилактики болезни"
                    " Альцгеймера (деменции). Лучший способ поддерживать Ваш процессор в рабочем состоянии найти"
                    " трудно. Тем более в наш век этот процесс можно сделать не скучным, интересным и бесплатным;"],
           ["Мозг", " Меняйте маршруты Вашего передвижения, любимые места, магазины и привычки. Однообразие и рутина"
                    " — друзья депрессии; Рекомендуем Вам воспользоваться навыком для Яндекс Алисы *Планировщик"
                    " прогулок*"],
           ["Мозг", "Играйте в компьютерные игры. Нет ничего полезного в том, что бы просиживать за ними часами, но"
                    " в разумных пределах они хорошо сказываются на внимании, концентрации и реакции"],
           ["Тонус, иммунитет и общее состояние организма", "делайте привычкой ежедневно проводить небольшую"
                                                            " утреннюю зарядку;"],
           ["Тонус, иммунитет и общее состояние организма", " Старайтесь как можно больше времени проводить"
                                                            " на свежем воздухе;"],
           ["Тонус, иммунитет и общее состояние организма", "Активный отдых всегда полезнее пассивного. Как с"
                                                            " физической точки зрения (при небольших нагрузках мышцы"
                                                            " придут в норму быстрее чем при отсутствии нагрузок) так"
                                                            " и с точки зрения психологии (любое созидание или"
                                                            " достижение какого-либо результата поднимает настроение"
                                                            " больше, чем просмотр телевизора на диване);"],
           ["Тонус, иммунитет и общее состояние организма", "При простуде или гриппе не сбивайте безопасную для"
                                                            " человека температуру (до 39,5 градусов) таблетками."
                                                            " Дайте иммунитету самому сделать свою работу. Исключением,"
                                                            " конечно же, являются сопутствующие хронические"
                                                            " заболевания;"],
           ["Тонус, иммунитет и общее состояние организма", "Не хочется этого признавать, но в России есть несколько"
                                                            " городов с очень плохой экологической обстановкой. Если Вы"
                                                            " живете в одном из таких городов подумайте, нет ли у Вас"
                                                            " вариантов перебраться жить подальше от источников вредных"
                                                            " выбросов"],
           ["Не бойтесь продовольствия с надписью ГМО", "То, что человечество не вымирает от голода несмотря на то,"
                                                        " что нас уже больше 7 миллиардов — это заслуга ГМО. Наконец,"
                                                        " главная причина не бояться ГМО в том, что продукты без ГМО"
                                                        " существуют разве что в девственных лесах Амазонии."]]


# Определяем функцию-обработчик обычных текстовых сообщений.
# У неё два параметра, сам бот и класс updater, принявший сообщение.


def text_request(update, context):
    # У объекта класса Updater есть поле message,
    # являющееся объектом сообщения.
    # У message есть поле text, содержащее текст полученного сообщения,
    # а также метод reply_text(str),
    # отсылающий ответ пользователю, от которого получено сообщение.
    update.message.reply_text(
        "Вы ввели несуществующую команду. Попробуйте ещё раз.")


# Напишем соответствующие функции для обработки команд.
def start(update, context):
    update.message.reply_text(
        "Привет! Я бот - медицинский помощник. Я умею предполагать, чем вы болеете по симптоммам заболевания,"
        "следить за параметрами вашего здоровья, давать советы для здоровья и показывать карту медицинских"
        " учреждений в  вашем городе.")
    time.sleep(1)
    update.message.reply_text(
        "Помните о том, что я не являюсь медицинским специалистом,"
        " поэтому вам следует посетить врача, чтобы он определил заболевание")
    time.sleep(1)
    update.message.reply_text(
        "Для получения большего количества информации введите команду /help")


def choose(update, context):
    a = context.args[0]
    global check_started
    if check_started == 1:
        ill_check(update, a)


def start_test(update, context):
    ill_check(update, '%^%')


def ill_check(update, a):
    global stage, check_started, answer
    if a == '%^%':
        stage = 0
        check_started = 1
    if stage == 0:
        answer = [0, 0, 0]
        update.message.reply_text('Сейчас вам нужно будет ответить на несколько вопросов, это поможет нам определить '
                                  'вашу болезнь')
        update.message.reply_text('Вам нужно будет выбирать один из 3 вариантов, написав /choose и символ (1,2,3) или '
                                  'любой другой символ, если ни один симптом не подходит')
        update.message.reply_text('Ухудшение самочувствия')
        update.message.reply_text('1) Постепенное')
        update.message.reply_text('2) Быстрое')
        update.message.reply_text('3) Внезапное')
        stage += 1
    elif stage == 1:
        if a == '1':
            answer[0] += 1
        elif a == '2':
            answer[1] += 1
        elif a == '3':
            answer[2] += 1
        stage += 1
        update.message.reply_text('Температура тела')
        update.message.reply_text('1) Около 37.5 градусов')
        update.message.reply_text('2) Около 38.5 градусов')
        update.message.reply_text('3) Больше 39 градусов')
        stage += 1
    elif stage == 2:
        if a == '1':
            answer[0] += 1
        elif a == '2':
            answer[1] += 1
        elif a == '3':
            answer[2] += 1
        update.message.reply_text('Интоксикация')
        update.message.reply_text('1) Не выражена')
        update.message.reply_text('2) Есть в виде повышенной утомляемости')
        update.message.reply_text('3) Есть, сильный озноб, головная боль, светобоязнь, ломота в теле')
        stage += 1
    elif stage == 3:
        if a == '1':
            answer[0] += 1
        elif a == '2':
            answer[1] += 1
        elif a == '3':
            answer[2] += 1
        update.message.reply_text('Чихание')
        update.message.reply_text('1) Есть нечасто')
        update.message.reply_text('2) Есть часто')
        update.message.reply_text('3) Нет')
        stage += 1
    elif stage == 4:
        if a == '1':
            answer[0] += 1
        elif a == '2':
            answer[1] += 1
        elif a == '3':
            answer[2] += 1
        update.message.reply_text('Боль в горле и его покраснение')
        update.message.reply_text('1) Только дискомфорт в горле')
        update.message.reply_text('2) Боль при кашле')
        update.message.reply_text('3) Постоянная боль, усиливающаяся при кашле')
        stage += 1
    elif stage == 5:
        if a == '1':
            answer[0] += 1
        elif a == '2':
            answer[1] += 1
        elif a == '3':
            answer[2] += 1
        update.message.reply_text('Головная боль')
        update.message.reply_text('1) Отсутствует')
        update.message.reply_text('2) Слабая')
        update.message.reply_text('3) Сильная')
        stage += 1
    elif stage == 6:
        if a == '1':
            answer[0] += 1
        elif a == '2':
            answer[1] += 1
        elif a == '3':
            answer[2] += 1
        update.message.reply_text('Боль в горле и его покраснение')
        update.message.reply_text('1) Только дискомфорт в горле')
        update.message.reply_text('2) Боль при кашле')
        update.message.reply_text('3) Постоянная боль, усиливающаяся при кашле')
        stage += 1
    elif stage == 7:
        if a == '1':
            answer[0] += 1
        elif a == '2':
            answer[1] += 1
        elif a == '3':
            answer[2] += 1
        update.message.reply_text('Повышенная утомляемость и бессоница')
        update.message.reply_text('1) Отсутствует')
        update.message.reply_text('2) Есть, слабо выражены и связаны с высокой температурой')
        update.message.reply_text('3) Есть, сильно выражены')
        stage += 1
    elif stage == 8:
        if a == '1':
            answer[0] += 1
        elif a == '2':
            answer[1] += 1
        elif a == '3':
            answer[2] += 1
        if answer[0] == answer[1] and answer[1] == answer[2] and answer[0] == 0:
            update.message.reply_text('Поздравляю! скорее всего вы не болеете респираторными заболеваниями')
        if max(answer) == answer[0]:
            update.message.reply_text('Скорее всего у вас простуда, рекомендуется сходить в аптеку и посоветоваться в'
                                      ' фармацевтом о лекарстве')
            update.message.reply_text('чтобы посмотреть карту аптек используйте команду /get_map название города')
        elif max(answer) == answer[1]:
            update.message.reply_text('Скорее всего у вас ОРВИ, рекомендуется сходить в больницу к терапевту')
            update.message.reply_text('чтобы посмотреть карту больниц используйте команду /get_map название города')
        elif max(answer) == answer[2]:
            update.message.reply_text('Скорее всего у вас Грипп, настоятельно рекомендуется сходить в больницу к '
                                      'терапевту для назначения лечения')
            update.message.reply_text('Грипп довольно опасное заболевание, поэтому чем раньше вы начнёте лечение, '
                                      'тем лучше')
            update.message.reply_text('чтобы посмотреть карту больниц используйте команду /get_map название города')


def add_params(update, context):
    while len(context.args) != 3:
        update.message.reply_text("Вы не ввели не все данные."
                                  " Введите /add_params <верхнее давление> <нижнее давление> <пульс>."
                                  "Например, /add_params 110 70 40")
        return

    # Создаём базу данных и таблицу в ней, если её ещё нет
    if os.path.exists('data/human_params/' + str(update.message.chat_id) + '.db') is False:
        con = sqlite3.connect('data/human_params/' + str(update.message.chat_id) + '.db')
        cursor = con.cursor()

        # создаём таблицу с нужными нам столбцами
        cursor.execute("""CREATE TABLE IF NOT EXISTS human_params(
           date TEXT,
           pressure TEXT,
           pulse TEXT);
        """)

        # вставляем данные в таблицу
        date_now = str(datetime.datetime.now())[:19]
        cursor.execute("INSERT INTO human_params VALUES(?, ?, ?)", (date_now, str(context.args[0]) + "/"
                                                                    + str(context.args[1]), str(context.args[2])))
        con.commit()
    else:
        con = sqlite3.connect('data/human_params/' + str(update.message.chat_id) + '.db')
        cursor = con.cursor()
        # вставляем данные в таблицу
        date_now = str(datetime.datetime.now())[:19]
        print(date_now, str(context.args[0]) + "/" + str(context.args[1]), str(context.args[2]))
        cursor.execute("""INSERT INTO human_params(date, pressure, pulse) VALUES(?, ?, ?)""",
                       (date_now, str(context.args[0]) + "/" + str(context.args[1]), str(context.args[2]))).fetchall()
        con.commit()

    update.message.reply_text("Принял!")


def get_params(update, context):
    if os.path.isfile('data/human_params/' + str(update.message.chat_id) + '.db'):
        con = sqlite3.connect('data/human_params/' + str(update.message.chat_id) + '.db')
        cursor = con.cursor()
        result = cursor.execute("""SELECT * FROM human_params""").fetchall()
        for i in result:
            update.message.reply_text("Дата: " + i[0] + " давление:" + i[1] + " пульс:" + i[2])
    else:
        update.message.reply_text("Вы не записывали параметры вашего здоровья.")


def clean_up(update, context):
    if os.path.isfile('data/human_params/' + str(update.message.chat_id) + '.db'):
        os.remove('data/human_params/' + str(update.message.chat_id) + '.db')
        update.message.reply_text("Удалил!")
    else:
        update.message.reply_text("Вы не записывали параметры вашего здоровья.")


def bot_help(update, context):
    update.message.reply_text(
        "Команда /start_test позволяет получить предположение от том, чем вы болеете.")
    time.sleep(1)
    update.message.reply_text(
        "Команда /get_map позволяет получить карту медицинкских учреждений."
        "Введите /get_map <название города>. Например, /get_map Москва")
    time.sleep(1)
    update.message.reply_text(
        "Команда /advice даёт полезный совет, который поможет вам сохранить здоровье.")
    time.sleep(1)
    update.message.reply_text(
        "Команда /add_params добавляет параметры вашего организма (верхнее и нижнее давление, пульс)."
        "Для использования введите /add_params <верхнее давление> <нижнее давление> <пульс>")
    time.sleep(1)
    update.message.reply_text(
        "Команда /get_params позволяет вам получить параметры, которые вы записывали."
        "Для использования введите /get_params ")
    time.sleep(1)
    update.message.reply_text(
        "Команда /clean_up позволяет вам очистить список введённых параметров."
        "Для использования введите /clean_up ")
    time.sleep(1)
    update.message.reply_text(
        "Для того, чтобы вернуть начать общение заново, введите команду /start.")


def set_med_time(update, context):
    while len(context.args) != 2:
        update.message.reply_text("Вы не ввели не все данные."
                                  " Введите /set_med_time <время напоминания> <дни недели (числа от 0 до 6)>."
                                  "Например, /set_med_time 18:00 0123456")
        return

    update.message.reply_text("Просим прощения, эта функция на данный момент находится в разработке.")
    # Приводим время к виду datetime.time
    # alarm_time = datetime.time(hour=int(context.args[0][:2]), minute=int(context.args[0][3:]), second=0)

    # Приводим дни недели к нужному виду
    # days_list = list(context.args[1])
    # days_tuple = tuple(int(item) for item in days_list)
    # prompt = update.job_queue.run_daily(reminder, alarm_time, days=days, context=None,
    #                                     name=None, job_kwargs=None)
    # context.job_queue.run_daily(reminder, alarm_time, days=days_tuple, context=update.message.chat_id,
    #                             name=str(update.message.chat_id), job_kwargs=None)


def reminder(update, context):
    update.message.reply_text("Не забудьте принять лекарство!")


def get_map(update, context):
    while len(context.args) != 1:
        update.message.reply_text("Вы не ввели название города. Введите /get_map <название города>."
                                  "Например, /get_map Москва")
        return

    # Получаем название города в виде аргумента команды
    global city
    city = context.args[0]

    # Создаём клавиатуру из кнопок
    get_map_keyboard = [['/pharmacy_map', '/hospital_map'],
                        ['/start']]
    get_map_markup = ReplyKeyboardMarkup(get_map_keyboard, one_time_keyboard=True)

    update.message.reply_text("Выберите, карту чего вы хотите получить. "
                              "Команда /pharmacy_map - карту аптек, "
                              "команда /hospital_map - карту больниц", reply_markup=get_map_markup)


def pharmacy_map(update, context):
    global city
    name_object = "аптека"
    chat_id = update.message.chat_id

    update.message.reply_text("Ищу...")

    # Создаём и отправляем запрос
    city_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" + city \
                   + "&format=json"
    city_response = requests.get(city_request).json()
    city_coord = city_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    coord = city_coord.split()
    string_coord = coord[0] + "," + coord[1]
    object_request = "https://search-maps.yandex.ru/v1/?text=" + name_object + "&type=biz&lang=ru_RU&ll=" \
                     + string_coord + "&spn=1,1&results=100&apikey=6633a817-a99a-4d17-b557-a77557303ccc"
    object_response = requests.get(object_request)
    json_response = object_response.json()
    map_request = "https://static-maps.yandex.ru/1.x/?ll=" + string_coord + "&spn=0.05,0.05&l=map,skl&pt="
    for i in json_response['features']:
        coord_object = i['geometry']['coordinates']
        map_request += str(coord_object[0]) + "," + str(coord_object[1]) + ",pm2rdl" + "~"
    map_request = map_request[:-1]
    print(map_request[:-1])

    context.bot.send_photo(
        chat_id,  # Идентификатор чата. Куда посылать картинку.
        # Ссылка на static API, по сути, ссылка на картинку.
        # Телеграму можно передать прямо её, не скачивая предварительно карту.
        map_request,
        caption="Нашёл:"
    )

    city = ""


def hospital_map(update, context):
    global city
    name_object = "больница"
    chat_id = update.message.chat_id

    update.message.reply_text("Ищу...")

    # Создаём и отправляем запрос
    city_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" + city \
                   + "&format=json"
    city_response = requests.get(city_request).json()
    city_coord = city_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    coord = city_coord.split()
    string_coord = coord[0] + "," + coord[1]
    object_request = "https://search-maps.yandex.ru/v1/?text=" + name_object + "&type=biz&lang=ru_RU&ll=" \
                     + string_coord + "&spn=1,1&results=100&apikey=6633a817-a99a-4d17-b557-a77557303ccc"
    object_response = requests.get(object_request)
    json_response = object_response.json()
    map_request = "https://static-maps.yandex.ru/1.x/?ll=" + string_coord + "&spn=0.05,0.05&l=map,skl&pt="
    for i in json_response['features']:
        coord_object = i['geometry']['coordinates']
        map_request += str(coord_object[0]) + "," + str(coord_object[1]) + ",pm2rdl" + "~"
    map_request = map_request[:-1]

    context.bot.send_photo(
        chat_id,  # Идентификатор чата. Куда посылать картинку.
        # Ссылка на static API, по сути, ссылка на картинку.
        # Телеграму можно передать прямо её, не скачивая предварительно карту.
        map_request,
        caption="Нашёл:"
    )

    city = ""


def advice(update, context):
    global advices
    # Получаем случайный элемент из списка с советами
    element = choice(advices)
    update.message.reply_text(element[0])
    update.message.reply_text(element[1])


def main():
    # Создаём объект updater.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    updater = Updater('1719672003:AAGr9uZu4-9thLycNUyaX39-dGjpHS7v8p8', use_context=True)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    # Создаём обработчик сообщений типа Filters.text
    # из описанной выше функции echo()
    # После регистрации обработчика в диспетчере
    # эта функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    text_handler = MessageHandler(Filters.text, text_request)
    # Регистрируем обработчик в диспетчере.
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", bot_help))
    dp.add_handler(CommandHandler("get_map", get_map, pass_args=True))
    dp.add_handler(CommandHandler("pharmacy_map", pharmacy_map))
    dp.add_handler(CommandHandler("hospital_map", hospital_map))
    dp.add_handler(CommandHandler("set_med_time", set_med_time, pass_args=True))
    dp.add_handler(CommandHandler("reminder", reminder))
    dp.add_handler(CommandHandler("get_params", get_params))
    dp.add_handler(CommandHandler("clean_up", clean_up))
    dp.add_handler(CommandHandler("choose", choose))
    dp.add_handler(CommandHandler("start_test", start_test))
    dp.add_handler(CommandHandler("add_params", add_params, pass_args=True))
    dp.add_handler(CommandHandler("advice", advice))
    dp.add_handler(text_handler)

    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()
    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
