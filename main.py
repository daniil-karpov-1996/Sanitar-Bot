# Импортируем необходимые библиотеки.
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import requests
import os
import datetime
import time
import os.path
import sqlite3
from random import choice

city = {}
users_active = {}
check_started = 0
ill_answer = {}
bekh_stage = {}
bekh_answer = {}
taylor_stage = {}
taylor_answer = {}
dass21_stage = {}
dass21_answer = {}


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
    update.message.reply_text("Вы ввели несуществующую команду. Попробуйте ещё раз.")


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

def check_num_for_bekh(text):
    checking_num = text
    k=0
    while k<10:
        if checking_num.isnumeric() and len(checking_num)==1:
            if int(checking_num)>=0 and int(checking_num)<=3:
                return int(checking_num)
    return 0

def start_test(update, context):
    bekh_test_keyboard = [['/start_ill_test', '/start_bekh_test'],
                          ['/start_taylor_test', '/start_dass21_test']]
    bekh_test_markup = ReplyKeyboardMarkup(bekh_test_keyboard, one_time_keyboard=True)
    update.message.reply_text("""вы можете пройти один из наших тестов на физическое или психическое
    состояние здоровья для этого выберите соответствующий тест при помощи одной из команд
    /start_ill_test - тест на болезни
    /start_bekh_test - тест бека на эмоциональное состояние
    /start_taylor_test - тест тейлора на эмоциональное состояние
    /start_dass21_test на эмоциональное состояние
    """, reply_markup=bekh_test_markup)


def start_bekh_test(update, context):
    global bekh_answer, bekh_stage
    bekh_test_keyboard = [['/bekh_test 0', '/bekh_test 1'],
                        ['/bekh_test 2', '/bekh_test 3']]
    bekh_test_markup = ReplyKeyboardMarkup(bekh_test_keyboard)
    update.message.reply_text("""Опросник состоит из 21 пункта. Каждый пункт включает один из симптомов тревоги
                телесных или психических. Оцените каждый пункт по шкале от 0 до 3 включительно, где 0 - 
                симптом не беспокиол, 3 - симптом беспокоил очень часто. Примерно время тестирования займёт 10 минут.
                Информация не является медицинским диагнозом. По поводу результатов теста необходимо
                проконсультироваться со специалистом""", reply_markup=bekh_test_markup)
    update.message.reply_text("""Чтобы выбрать вариант напишите /bekh_test номер варианта
    или воспользуйтесь кнопками снизу""")
    bekh_answer[update.message.chat_id] = 0
    bekh_stage[update.message.chat_id] = 0
    bekh_test(update, context='start')

def bekh_test(update, context):
    questions = ['Ощущение онемения или покалывания в теле', 'Ощущение жары', 'Дрожь в ногах',
                 'Неспособность расслабиться', 'Страх, что произойдет самое плохое',
                 'Головокружение или ощущение легкости в голове', 'Ускоренное сердцебиение', 'Неустойчивость',
                 'Ощущение ужаса', 'Нервозность', 'Дрожь в руках', 'Ощущение удушья',
                 'Шаткость походки', 'Страх утраты контроля', 'Затрудненность дыхания',
                 'Страх смерти', 'Испуг', 'Желудочно-кишечные расстройства', 'Обмороки', 'Приливы крови к лицу',
                 'Усиление потоотделения (не связанное с жарой)']
    if context == 'start':
        i = bekh_stage[update.message.chat_id]
        update.message.reply_text(str(i + 1) + '/21 ' + questions[i])
        bekh_stage[update.message.chat_id] += 1
    if context != 'start':
        if bekh_stage[update.message.chat_id] == 21:
            update.message.reply_text('Конец теста', reply_markup=ReplyKeyboardRemove())
            time.sleep(1)
            update.message.reply_text('Ваш результат:')
            time.sleep(1)
            if bekh_answer[update.message.chat_id]<10:
                update.message.reply_text('У вас отсутсвует тревого')
            elif bekh_answer[update.message.chat_id]<22:
                update.message.reply_text('У вас незначительный уровень тревоги')
            elif bekh_answer[update.message.chat_id]<36:
                update.message.reply_text('У вас средней уровень тревоги, советуем обратиться к специалисту')
            else:
                update.message.reply_text('У вас высокий уровеноь тревоги, советуем незамедлительно обратиться к врачу')
        else:
            i = bekh_stage[update.message.chat_id]
            update.message.reply_text(str(i + 1) + '/21 ' + questions[i])
            bekh_answer[update.message.chat_id] += check_num_for_bekh(context.args[0])
            bekh_stage[update.message.chat_id] += 1


def start_taylor_test(update, context):
    global taylor_answer, taylor_stage
    taylor_test_keyboard = [['/taylor_test да', '/taylor_test нет']]
    taylor_test_markup = ReplyKeyboardMarkup(taylor_test_keyboard)
    update.message.reply_text('''Опросник состоит из 50 вопросов, на которые следует отвечать только да или нет. Опросник покажет
    ваш уровень трежности. Информация не является медицинским диагнозом. По поводу результатов теста необходимо
    проконсультироваться со специалистом''', reply_markup=taylor_test_markup)
    update.message.reply_text("""Чтобы выбрать вариант напишите /taylor_test вариант ответа:да или нет.
    или воспользуйтесь кнопками снизу""")
    taylor_answer[update.message.chat_id] = 0
    taylor_stage[update.message.chat_id] = 0
    taylor_test(update, context='start')

def taylor_test(update, context):
    questions = ['Обычно я спокоен и вывести меня из себя нелегко.',
'Мои нервы расстроены не более, чем у других людей.',
'У меня редко бывают запоры.',
'У меня редко бывают головные боли.',
'Я редко устаю.',
'Я почти всегда чувствую себя вполне счастливым.',
'Я уверен в себе.',
'Практически я никогда не краснею.',
'По сравнению со своими друзьями я считаю себя вполне смелым человеком.',
'Я краснею не чаще, чем другие.',
'У меня редко бывает сердцебиение.',
'Обычно мои руки достаточно теплые.',
'Я застенчив не более чем другие.',
'Мне не хватает уверенности в себе.',
'Порой мне кажется, что я ни на что не годен.',
'У меня бывают периоды такого беспокойства, что я не могу усидеть на месте.',
'Мой желудок сильно беспокоит меня.',
'У меня хватает духа вынести все предстоящие трудности.',
'Я хотел бы быть таким же счастливым, как другие.',
'Мне кажется порой, что передо мной нагромождены такие трудности, которые мне не преодолеть.',
'Мне нередко снятся кошмарные сны.',
'Я замечаю, что мои руки начинают дрожать, когда я пытаюсь что-либо сделать.',
'У меня чрезвычайно беспокойный и прерывистый сон.',
'Меня весьма тревожат возможные неудачи.',
'Мне приходилось испытывать страх в тех случаях, когда я точно знал, что мне ничто не угрожает.',
'Мне трудно сосредоточиться на работе или на каком-либо задании.',
'Я работаю с большим напряжением.',
'Я легко прихожу в замешательство.',
'Почти все время испытываю тревогу из-за кого-либо или из-за чего-либо.',
'Я склонен принимать все слишком всерьез.',
'Я часто плачу.',
'Меня нередко мучают приступы рвоты и тошноты.',
'Раз в месяц или чаще у меня бывает расстройство желудка.',
'Я часто боюсь, что вот-вот покраснею.',
'Мне очень трудно сосредоточиться на чем-либо.',
'Мое материальное положение весьма беспокоят меня.',
'Нередко я думаю о таких вещах, о которых ни с кем не хотелось бы говорить.',
'У меня бывали периоды, когда тревога лишала меня сна.',
'Временами, когда я нахожусь в замешательстве, у меня появляется сильная потливость, что очень смущает меня.',
'Даже в холодные дни я легко потею.',
'Временами я становлюсь таким возбужденным, что мне трудно заснуть.',
'Я - человек легко возбудимый.',
'Временами я чувствую себя совершенно бесполезным.',
'Порой мне кажется, что мои нервы сильно расшатаны, и я вот - вот выйду из себя.',
'Я часто ловлю себя на том, что меня что-то тревожит.',
'Я гораздо чувствительнее, чем большинство других людей.',
'Я почти все время испытываю чувство голода.',
'Ожидание меня нервирует.',
'Жизнь для меня связана с необычным напряжением.',
'Ожидание всегда нервирует меня.']
    yes_balls = [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                  29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    no_balls = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    if context == 'start':
        i = taylor_stage[update.message.chat_id]
        update.message.reply_text(str(i+1) + '/50 ' + questions[i])
        taylor_stage[update.message.chat_id] += 1
    else:
        if taylor_stage[update.message.chat_id] == 50:
            update.message.reply_text('Конец теста', reply_markup=ReplyKeyboardRemove())
            time.sleep(1)
            update.message.reply_text('Ваш результат:')
            time.sleep(1)
            if taylor_answer[update.message.chat_id] < 6:
                update.message.reply_text('У вас низкий уровень тревоги или её нет')
            elif taylor_answer[update.message.chat_id] < 15:
                update.message.reply_text('У вас средний уровень тревоги с тенденцией к низкому. Советуем больше отдыхать')
            elif taylor_answer[update.message.chat_id] < 25:
                update.message.reply_text('У вас средний увроень тревоги с тенденцией к высокому. Советуем обратиться к специалисту')
            elif taylor_answer[update.message.chat_id] < 40:
                update.message.reply_text('У вас высокий уровень тревоги. Советуем в ближайшее время обратиться к специалисту')
            else:
                update.message.reply_text('У вас очень высокий уровень тревоги. Обратитесь к специалисту как можно скорее')
        else:
            i = taylor_stage[update.message.chat_id]
            update.message.reply_text(str(i + 1) + '/50 ' + questions[i])
            taylor_stage[update.message.chat_id] += 1
            text = context.args[0]
            if text.lower()=='да':
                text = 1
            else:
                text = 0
            if (text == 1 and ((i+1) in yes_balls)) or (text == 0 and ((i+1) in no_balls)):
                taylor_answer[update.message.chat_id]+=1


def start_dass21_test(update, context):
    global dass21_answer, dass21_stage
    dass21_test_keyboard = [['/dass21_test 0', '/dass21_test 1'],
                          ['/dass21_test 2', '/dass21_test 3']]
    dass21_test_markup = ReplyKeyboardMarkup(dass21_test_keyboard)
    update.message.reply_text('''Внимательно прочитайте каждое утверждение и выберите цифру от 0 до 3, которая лучше всего
    описывает то, как утверждение соотносится с вами.
     0 - вообще не относится ко мне,
     1 - Относилось ко мне до некоторой степени или некоторое время,
     2 - Относилось ко мне в значительной мере или значительную часть времени, 
     3 -  Относилось ко мне полностью или большую часть времени
    Не размышляйте слишком долго, в тесте нет «правильных» или
    «неправильных» ответов. Результат не является клиническим диангнозом и требует консультации специалисти''',
    reply_markup=dass21_test_markup)
    update.message.reply_text("""Чтобы выбрать вариант напишите /dass21_test номер варианта
        или воспользуйтесь кнопками снизу""")
    dass21_answer[update.message.chat_id] = [0, 0, 0]
    dass21_stage[update.message.chat_id] = 0
    dass21_test(update, context='start')

def dass21_test(update, context):
    questions = [
        'Мне было трудно сбросить напряжение.',
        'Я ощущал сухость во рту.',
        'Я вообще не испытывал никаких положительных чувств.',
        'Я ощущал, что мое дыхание затруднено (например, чрезвычайно быстрое дыхание, одышка в отсутствие физических нагрузок).',
        'Мне было трудно заставить себя сделать что-либо.',
        'Я был склонен слишком сильно реагировать на ситуацию.',
        'Я ощущал тремор (например, в руках).',
        'Я чувствовал, что трачу слишком много нервной энергии.',
        'Меня беспокоили ситуации, в которых я могу поддаться панике и вести себя глупо.',
        'Я чувствовал, что у меня нет ничего впереди.',
        'Я чувствовал растущее волнение.',
        'Мне было трудно расслабиться.',
        'Я чувствовал упадок духа и меланхолию.',
        'Я нетерпимо относился ко всему, что мешало мне заниматься тем, что я делаю.',
        'Я ощущал, что я близок к панике.',
        'Я был не в состоянии проявлять энтузиазм по отношению к чему-либо.',
        'Я чувствовал, что немногого стою как личность.',
        'Я чувствовал, что был весьма раздражителен.',
        'Я замечал, что происходит с моим сердцем без всяких физических нагрузок (например, ощущение усиливающегося сердцебиения или пропущенного удара).',
        'Я ощущал беспричинный страх.',
        'Я чувствовал, что жизнь бессмысленна.'
    ]
    d_questions = [1, 2, 4, 6, 7, 8, 9, 11, 12, 14, 15, 18, 19, 20]
    a_questions = [1, 3, 5, 6, 8, 10, 11, 12, 13, 14, 16, 17, 18, 21]
    s_questions = [2, 3, 4, 5, 7, 9, 10, 13, 15, 16, 17, 19, 20, 21]
    d_summa = 0
    a_summa = 0
    s_summa = 0
    if context == 'start':
        i = dass21_stage[update.message.chat_id]
        update.message.reply_text(str(i + 1) + '/21 ' + questions[i])
        dass21_stage[update.message.chat_id] += 1
    else:
        a_summa = dass21_answer[update.message.chat_id][0]
        d_summa = dass21_answer[update.message.chat_id][1]
        s_summa = dass21_answer[update.message.chat_id][2]
        if dass21_stage[update.message.chat_id] == 21:
            update.message.reply_text('Конец теста', reply_markup=ReplyKeyboardRemove())
            time.sleep(1)
            update.message.reply_text('Ваш результат:')
            time.sleep(1)
            if d_summa < 5:
                update.message.reply_text('У вас нормальный показатель, депрессии нет')
            elif d_summa < 7:
                update.message.reply_text('У вас лёгкий показатель депрессии')
            elif d_summa < 11:
                update.message.reply_text('У вас средний показатель депрессии')
            elif d_summa < 14:
                update.message.reply_text('У вас сильный показатель депрессии')
            else:
                update.message.reply_text('У вас очень сильный показатель депрессии')

            if a_summa < 4:
                update.message.reply_text('У вас нормальный показатель тревожности')
            elif a_summa < 6:
                update.message.reply_text('У вас лёгкий покатель тревожности')
            elif a_summa < 8:
                update.message.reply_text('У вас средний показатель тревожности')
            elif a_summa < 10:
                update.message.reply_text('У вас сильный показатель тревожности')
            else:
                update.message.reply_text('У вас очень сильный показатель тревожности')

            if s_summa < 8:
                update.message.reply_text('У вас нормальный показатель стресса')
            elif s_summa < 10:
                update.message.reply_text('У вас лёгкий показатель стресса')
            elif s_summa < 13:
                update.message.reply_text('У вас средний показатель стресса')
            elif s_summa < 17:
                update.message.reply_text('У вас сильный показатель стресса')
            else:
                update.message.reply_text('У вас очень сильный показатель стресса')
        else:
            i = dass21_stage[update.message.chat_id]
            update.message.reply_text(str(i + 1) + '/21 ' + questions[i])
            dass21_stage[update.message.chat_id] += 1
            answer = context.args[0]
            if i + 1 in a_questions:
                a_summa += int(answer)
            if i + 1 in d_questions:
                d_summa += int(answer)
            if i + 1 in s_questions:
                s_summa += int(answer)
            dass21_answer[update.message.chat_id] = [a_summa, d_summa, s_summa]


def ill_choose(update, context):
    if context.args == []:
        a = -1
    else:
        a = context.args[0]
    global check_started
    if check_started == 1:
        ill_check(update, a)


def start_ill_test(update, context):
    ill_test_keyboard = [['/ill_choose 0', '/ill_choose 1'],
                          ['/ill_choose 2', '/ill_choose 3']]
    ill_test_markup = ReplyKeyboardMarkup(ill_test_keyboard)
    update.message.reply_text('Сейчас вам нужно будет ответить на несколько вопросов, это поможет нам определить '
                              'вашу болезнь', reply_markup=ill_test_markup)
    global users_active
    ill_check(update, '%^%')


def ill_check(update, a):
    global check_started, ill_answer, users_active
    if a == '%^%':
        users_active[update.message.chat_id] = 0
        ill_answer[update.message.chat_id] = [0, 0, 0]
        check_started = 1
    if users_active[update.message.chat_id] == 0:
        ill_answer[update.message.chat_id] = [0, 0, 0]
        update.message.reply_text('Вам нужно будет выбирать один из 3 вариантов, написав /ill_choose и символ (1,2,3) или '
                                  'любой другой символ, если ни один симптом не подходит')
        update.message.reply_text('Ухудшение самочувствия')
        update.message.reply_text('1) Постепенное')
        update.message.reply_text('2) Быстрое')
        update.message.reply_text('3) Внезапное')
        users_active[update.message.chat_id] += 1
    elif users_active[update.message.chat_id] == 1:
        if a == '1':
            ill_answer[update.message.chat_id][0] += 1
        elif a == '2':
            ill_answer[update.message.chat_id][1] += 1
        elif a == '3':
            ill_answer[update.message.chat_id][2] += 1
        update.message.reply_text('Температура тела')
        update.message.reply_text('1) Около 37.5 градусов')
        update.message.reply_text('2) Около 38.5 градусов')
        update.message.reply_text('3) Больше 39 градусов')
        users_active[update.message.chat_id] += 1
    elif users_active[update.message.chat_id] == 2:
        if a == '1':
            ill_answer[update.message.chat_id][0] += 1
        elif a == '2':
            ill_answer[update.message.chat_id][1] += 1
        elif a == '3':
            ill_answer[update.message.chat_id][2] += 1
        update.message.reply_text('Интоксикация')
        update.message.reply_text('1) Не выражена')
        update.message.reply_text('2) Есть в виде повышенной утомляемости')
        update.message.reply_text('3) Есть, сильный озноб, головная боль, светобоязнь, ломота в теле')
        users_active[update.message.chat_id] += 1
    elif users_active[update.message.chat_id] == 3:
        if a == '1':
            ill_answer[update.message.chat_id][0] += 1
        elif a == '2':
            ill_answer[update.message.chat_id][1] += 1
        elif a == '3':
            ill_answer[update.message.chat_id][2] += 1
        update.message.reply_text('Чихание')
        update.message.reply_text('1) Есть нечасто')
        update.message.reply_text('2) Есть часто')
        update.message.reply_text('3) Нет')
        users_active[update.message.chat_id] += 1
    elif users_active[update.message.chat_id] == 4:
        if a == '1':
            ill_answer[update.message.chat_id][0] += 1
        elif a == '2':
            ill_answer[update.message.chat_id][1] += 1
        elif a == '3':
            ill_answer[update.message.chat_id][2] += 1
        update.message.reply_text('Боль в горле и его покраснение')
        update.message.reply_text('1) Только дискомфорт в горле')
        update.message.reply_text('2) Боль при кашле')
        update.message.reply_text('3) Постоянная боль, усиливающаяся при кашле')
        users_active[update.message.chat_id] += 1
    elif users_active[update.message.chat_id] == 5:
        if a == '1':
            ill_answer[update.message.chat_id][0] += 1
        elif a == '2':
            ill_answer[update.message.chat_id][1] += 1
        elif a == '3':
            ill_answer[update.message.chat_id][2] += 1
        update.message.reply_text('Головная боль')
        update.message.reply_text('1) Отсутствует')
        update.message.reply_text('2) Слабая')
        update.message.reply_text('3) Сильная')
        users_active[update.message.chat_id] += 1
    elif users_active[update.message.chat_id] == 6:
        if a == '1':
            ill_answer[update.message.chat_id][0] += 1
        elif a == '2':
            ill_answer[update.message.chat_id][1] += 1
        elif a == '3':
            ill_answer[update.message.chat_id][2] += 1
        update.message.reply_text('Повышенная утомляемость и бессоница')
        update.message.reply_text('1) Отсутствует')
        update.message.reply_text('2) Есть, слабо выражены и связаны с высокой температурой')
        update.message.reply_text('3) Есть, сильно выражены')
        users_active[update.message.chat_id] += 1
    elif users_active[update.message.chat_id] == 7:
        if a == '1':
            ill_answer[update.message.chat_id][0] += 1
        elif a == '2':
            ill_answer[update.message.chat_id][1] += 1
        elif a == '3':
            ill_answer[update.message.chat_id][2] += 1
        update.message.reply_text('Конец теста', reply_markup=ReplyKeyboardRemove())
        time.sleep(1)
        update.message.reply_text('Ваш результат:')
        time.sleep(1)
        if ill_answer[update.message.chat_id][0] == ill_answer[update.message.chat_id][1] and ill_answer[update.message.chat_id][
            1] == ill_answer[update.message.chat_id][2] and ill_answer[update.message.chat_id][0] == 0:
            update.message.reply_text('Поздравляю! скорее всего вы не болеете респираторными заболеваниями')
        if max(ill_answer[update.message.chat_id]) == ill_answer[update.message.chat_id][0]:
            update.message.reply_text('Скорее всего у вас простуда, рекомендуется сходить в аптеку и посоветоваться в'
                                      ' фармацевтом о лекарстве')
            update.message.reply_text('чтобы посмотреть карту аптек используйте команду /get_map название города')
        elif max(ill_answer[update.message.chat_id]) == ill_answer[update.message.chat_id][1]:
            update.message.reply_text('Скорее всего у вас ОРВИ, рекомендуется сходить в больницу к терапевту')
            update.message.reply_text('чтобы посмотреть карту больниц используйте команду /get_map название города')
        elif max(ill_answer[update.message.chat_id]) == ill_answer[update.message.chat_id][2]:
            update.message.reply_text('Скорее всего у вас Грипп, настоятельно рекомендуется сходить в больницу к '
                                      'терапевту для назначения лечения')
            update.message.reply_text('Грипп довольно опасное заболевание, поэтому чем раньше вы начнёте лечение, '
                                      'тем лучше')
            update.message.reply_text('чтобы посмотреть карту больниц используйте команду /get_map название города')


def add_params(update, context):
    while len(context.args) != 3:
        update.message.reply_text("Вы не ввели не все данные."
                                  " Введите /add_params <верхнее давление> <нижнее давление> <пульс>."
                                  "Например, /add_params 117 77 70")
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
        "Команда /start_test позволяет получить предположение о физическом или психическом состоянии здоровья")
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


def reminder(update, context):
    update.message.reply_text("Не забудьте принять лекарство!")


def get_map(update, context):
    while len(context.args) != 1:
        update.message.reply_text("Вы не ввели название города. Введите /get_map <название города>."
                                  "Например, /get_map Москва")
        return
    get_map_keyboard = [['/pharmacy_map', '/hospital_map']]
    get_map_markup = ReplyKeyboardMarkup(get_map_keyboard, one_time_keyboard=True)
    # Получаем название города в виде аргумента команды
    global city
    city[update.message.chat_id] = context.args[0]

    update.message.reply_text("Выберите, карту чего вы хотите получить. "
                              "Команда /pharmacy_map - карту аптек, "
                              "команда /hospital_map - карту больниц", reply_markup=get_map_markup)


def pharmacy_map(update, context):
    global city
    name_object = "аптека"
    chat_id = update.message.chat_id
    update.message.reply_text("Ищу...")
    # Создаём и отправляем запрос
    city_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" + city[
        update.message.chat_id] \
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


def hospital_map(update, context):
    global city
    name_object = "больница"
    chat_id = update.message.chat_id

    update.message.reply_text("Ищу...")

    # Создаём и отправляем запрос
    city_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" + city[
        update.message.chat_id] \
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


def advice(update, context):
    global advices
    # Получаем случайный элемент из списка с советами
    element = choice(advices)
    update.message.reply_text(element[0])
    update.message.reply_text(element[1])


def main():
    # Создаём объект updater.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    updater = Updater('5894989975:AAHQ3q-2pnb2GvrdkmUDbfVfyHGthfHHCs4', use_context=True)
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
    dp.add_handler(CommandHandler("get_params", get_params))
    dp.add_handler(CommandHandler("clean_up", clean_up))
    dp.add_handler(CommandHandler("ill_choose", ill_choose))
    dp.add_handler(CommandHandler("start_test", start_test))
    dp.add_handler(CommandHandler("start_ill_test", start_ill_test))
    dp.add_handler(CommandHandler("start_bekh_test", start_bekh_test))
    dp.add_handler(CommandHandler("bekh_test", bekh_test))
    dp.add_handler(CommandHandler("start_taylor_test", start_taylor_test))
    dp.add_handler(CommandHandler("taylor_test", taylor_test))
    dp.add_handler(CommandHandler("start_dass21_test", start_dass21_test))
    dp.add_handler(CommandHandler("dass21_test", dass21_test))
    dp.add_handler(CommandHandler("add_params", add_params, pass_args=True))
    dp.add_handler(CommandHandler("advice", advice))
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
