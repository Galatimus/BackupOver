#!/usr/bin/python
# -*- coding: utf-8 -*-

conv =[(u'Абакан',u'Республика Хакасия'),
    (u'Александров',u'Владимирская область'),
    (u'Абинск',u'Краснодарский край'),
    (u'Азнакаево',u'Татарстан'),
    (u'Азов',u'Ростовская область'),
    (u'Аксай',u'Ростовская область'),
    (u'Алатырь',u'Чувашия'),
    (u'Алейск',u'Алтайский край'),
    (u'Алексеевка',u'Белгородская область'),
    (u'Анива',u'Сахалинская область'),
    (u'Апатиты',u'Мурманская область'),
    (u'Апшеронск',u'Краснодарский край'),
    (u'Арамиль',u'Свердловская область'),
    (u'Ардатов',u'Мордовия'),
    (u'Ахтубинск',u'Астраханская область'),
    (u'Бакал',u'Челябинская область'),
    (u'Баксан',u'Кабардино-Балкария'),
    (u'Балашов',u'Саратовская область'),
    (u'Барыш',u'Ульяновская область'),
    (u'Белая Калитва',u'Ростовская область'),
    (u'Белев',u'Тульская область'),
    (u'Белореченск',u'Краснодарский край'),
    (u'Богучаны',u'Красноярский край'),
    (u'Богучар',u'Воронежская область'),
    (u'Бор',u'Нижегородская область'),
    (u'Бугульма',u'Татарстан'),
    (u'Бугуруслан',u'Оренбургская область'),
    (u'Бузулук',u'Оренбургская область'),
    (u'Вельск',u'Архангельская область'),
    (u'Верещагино',u'Пермский край'),
    (u'Вичуга',u'Ивановская область'),
    (u'Волхов',u'Ленинградская область'),
    (u'Всеволожск',u'Ленинградская область'),
    (u'Вятские Поляны',u'Кировская область'),
    (u'Гай',u'Оренбургская область'),
    (u'Георгиевск',u'Ставропольский край'),
    (u'Городище',u'Московская область'),
    (u'Гусь-Хрустальный',u'Московская область'),
    (u'Дзержинск',u'Нижегородская область'),
    (u'Дзержинский',u'Московская область'),
    (u'Димитровград',u'Ульяновская область'),
    (u'Долгопрудный',u'Московская область'),
    (u'Дюртюли',u'Башкортостан'),
    (u'Егорьевск',u'Московская область'),
    (u'Енисейск',u'Красноярский край'),
    (u'Ершов',u'Саратовская область'),
    (u'Ефремов',u'Тульская область'),
    (u'Железноводск',u'Ставропольский край'),
    (u'Задонск',u'Липецкая область'),
    (u'Заозерный',u'Красноярский край'),
    (u'Заринск',u'Алтайский край'),
    (u'Зверево',u'Ростовская область'),
    (u'Зеленокумск',u'Ставропольский край'),
    (u'Знаменск',u'Астраханская область'),
    (u'Зуевка',u'Кировская область'),
    (u'Ипатово',u'Ставропольский край'),
    (u'Искитим',u'Новосибирская область'),
    (u'Ишим',u'Тюменская область'),
    (u'Камызяк',u'Астраханская область'),
    (u'Канск',u'Красноярский край'),
    (u'Карачаевск',u'Карачаево-Черкесия'),
    (u'Кашира',u'Московская область'),
    (u'Кимры',u'Тверская область'),
    (u'Кинель',u'Самарская область'),
    (u'Кинешма',u'Ивановская область'),
    (u'Киреевск',u'Тульская область'),
    (u'Козьмодемьянск',u'Марий Эл'),
    (u'Константиновск',u'Ростовская область'),
    (u'Копейск',u'Челябинская область'),
    (u'Кореновск',u'Краснодарский край'),
    (u'Королёв',u'Московская область'),
    (u'Котельники',u'Московская область'),
    (u'Краснокаменск',u'Забайкальский край'),
    (u'Краснослободск',u'Волгоградская область'),
    (u'Красный Сулин',u'Ростовская область'),
    (u'Кропоткин',u'Краснодарский край'),
    (u'Кумертау',u'Башкортостан'),
    (u'Кызыл',u'Тыва'),
    (u'Лангепас',u'Ханты-Мансийский автономный округ — Югра'),
    (u'Ликино-Дулево',u'Московская область'),
    (u'Лихославль',u'Тверская область'),
    (u'Лыткарино',u'Московская область'),
    (u'Магас',u'Ингушетия'),
    (u'Майкоп',u'Адыгея'),
    (u'Мантурово',u'Костромская область'),
    (u'Мариинск',u'Кемеровская область'),
    (u'Междуреченск',u'Кемеровская область'),
    (u'Миасс',u'Челябинская область'),
    (u'Минеральные Воды',u'Ставропольский край'),
    (u'Минусинск',u'Красноярский край'),
    (u'Михайлов',u'Рязанская область'),
    (u'Михайловск',u'Ставропольский край'),
    (u'Москвы',u'Москва'),
    (u'Мценск',u'Орловская область'),
    (u'Мыски',u'Кемеровская область'),
    (u'Никольское',u'Сахалинская область'),
    (u'Новомосковск',u'Тульская область'),
    (u'Новый Уренгой',u'Ямало-Ненецкий автономный округ'),
    (u'Ногинск',u'Московская область'),
    (u'Норильск',u'Красноярский край'),
    (u'Нягань',u'Ханты-Мансийский автономный округ — Югра'),
    (u'Октябрьский',u'Башкортостан'),
    (u'Остров',u'Псковская область'),
    (u'Павлово',u'Нижегородская область'),
    (u'Павловск',u'Воронежская область'),
    (u'Пласт',u'Челябинская область'),
    (u'Порхов',u'Псковская область'),
    (u'Починок',u'Смоленская область'),
    (u'Приозерск',u'Ленинградская область'),
    (u'Пролетарск',u'Ростовская область'),
    (u'Радужный',u'Ханты-Мансийский автономный округ — Югра'),
    (u'Реутов',u'Московская область'),
    (u'Ростов',u'Ярославская область'),
    (u'Ростове-на-Дону',u'Ростовская область'),
    (u'Рудня',u'Смоленская область'),
    (u'Ряжск',u'Рязанская область'),
    (u'Салехард',u'Ямало-Ненецкий автономный округ'),
    (u'Сальск',u'Ростовская область'),
    (u'Светлоград',u'Ставропольский край'),
    (u'Северодвинск',u'Архангельская область'),
    (u'Североуральск',u'Свердловская область'),
    (u'Семенов',u'Нижегородская область'),
    (u'Сенгилей',u'Ульяновская область'),
    (u'Собинка',u'Владимирская область'),
    (u'Соликамск',u'Пермский край'),
    (u'Строитель',u'Белгородская область'),
    (u'Суджа',u'Курская область'),
    (u'Суздаль',u'Владимирская область'),
    (u'Сухой Лог',u'Свердловская область'),
    (u'Сходня',u'Московская область'),
    (u'Тейково',u'Ивановская область'),
    (u'Торопец',u'Тверская область'),
    (u'Урай',u'Ханты-Мансийский автономный округ — Югра'),
    (u'Усинск',u'Республика Коми'),
    (u'Усмань',u'Липецкая область'),
    (u'Ханты-Мансийск',u'Ханты-Мансийский автономный округ — Югра'),
    (u'Хасавюрт',u'Дагестан'),
    (u'Чебаркуль',u'Челябинская область'),
    (u'Черемхово',u'Иркутская область'),
    (u'Чехов',u'Московская область'),
    (u'Шахты',u'Ростовская область'),
    (u'Элиста',u'Калмыкия'),
    (u'Южноуральск',u'Челябинская область'),
    (u'Юрьев-Польский',u'Владимирская область'),
    (u'Яровое',u'Алтайский край'),
    (u'Ясногорск',u'Тульская область'),
    (u'Алексин',u'Тульская область'),
    (u'Алупка',u'Крым'),
    (u'Алушта',u'Крым'),
    (u'Альметьевск',u'Татарстан'),
    (u'Амурск',u'Хабаровский край'),
    (u'Анапа',u'Краснодарский край'),
    (u'Ангарск',u'Иркутская область'),
    (u'Арзамас',u'Нижегородская область'),
    (u'Армавир',u'Краснодарский край'),
    (u'Арсеньев',u'Приморский край'),
    (u'Артем',u'Приморский край'),
    (u'Архангельск',u'Архангельская область'),
    (u'Астрахань',u'Астраханская область'),
    (u'Ачинск',u'Красноярский край'),
    (u'Балаково',u'Саратовская область'),
    (u'Балашиха',u'Московская область'),
    (u'Барнаул',u'Алтайский край'),
    (u'Батайск',u'Ростовская область'),
    (u'Бахчисарай',u'Крым'),
    (u'Белгород',u'Белгородская область'),
    (u'Белокуриха',u'Алтайский край'),
    (u'Белорецк',u'Башкортостан'),
    (u'Бийск',u'Алтайский край'),
    (u'Бикин',u'Хабаровский край'),
    (u'Биробиджан',u'Еврейская автономная область'),
    (u'Благовещенск',u'Амурская область'),
    (u'Богородск',u'Нижегородская область'),
    (u'Большой Камень',u'Приморский край'),
    (u'Боровичи',u'Новгородская область'),
    (u'Боровск',u'Калужская область'),
    (u'Братск',u'Иркутская область'),
    (u'Бронницы',u'Московская область'),
    (u'Брянск',u'Брянская область'),
    (u'Великие Луки',u'Псковская область'),
    (u'Великий Новгород',u'Новгородская область'),
    (u'Венев',u'Тульская область'),
    (u'Верея',u'Московская область'),
    (u'Верхняя Пышма',u'Свердловская область'),
    (u'Видное',u'Московская область'),
    (u'Вилючинск',u'Камчптский край'),
    (u'Владивосток',u'Приморский край'),
    (u'Владикавказ',u'Республика Северная Осетия-Алания'),
    (u'Владимир',u'Владимирская область'),
    (u'Волгоград',u'Волгоградская область'),
    (u'Волгодонск',u'Ростовская область'),
    (u'Волжский',u'Волгоградская область'),
    (u'Вологда',u'Вологодская область'),
    (u'Волоколамск',u'Московская область'),
    (u'Воронеж',u'Воронежская область'),
    (u'Воткинск',u'Удмуртская республика'),
    (u'Выборг',u'Ленинградская область'),
    (u'Выкса',u'Нижегородская область'),
    (u'Вяземский',u'Хабаровский край'),
    (u'Вязники',u'Владимирская область'),
    (u'Геленджик',u'Краснодарский край'),
    (u'Горно-Алтайск',u'Республика Алтай'),
    (u'Грозный',u'Чеченская Республика'),
    (u'Дальнереченск',u'Приморский край'),
    (u'Дивногорск',u'Красноярский край'),
    (u'Дмитров',u'Московская область'),
    (u'Домодедово',u'Московская область'),
    (u'Евпатория',u'Крым'),
    (u'Ейск',u'Краснодарский край'),
    (u'Екатеринбург',u'Свердловская область'),
    (u'Елизово',u'Камчптский край'),
    (u'Ессентуки',u'Ставропольский край'),
    (u'Железнодорожный',u'Московская область'),
    (u'Жуковский',u'Московская область'),
    (u'Зеленоград',u'Москва'),
    (u'Зерноград',u'Ростовская область'),
    (u'Зерноград',u'Ростовская область'),
    (u'Златоуст',u'Челябинская область'),
    (u'Зубцов',u'Тверская область'),
    (u'Иваново',u'Ивановская область'),
    (u'Ивантеевка',u'Московская область'),
    (u'Ижевск',u'Удмуртская республика'),
    (u'Иркутск',u'Иркутская область'),
    (u'Истра',u'Московская область'),
    (u'Йошкар-Ола',u'Республика Марий Эл'),
    (u'Казань',u'Республика Татарстан'),
    (u'Калач-на-Дону',u'Волгоградская область'),
    (u'Калининград',u'Калининградская область'),
    (u'Калуга',u'Калужская область'),
    (u'Калязин',u'Тверская область'),
    (u'Каменск-Уральский',u'Свердловская область'),
    (u'Каменск-Шахтинский',u'Ростовская область'),
    (u'Камышин',u'Волгоградская область'),
    (u'Каспийск',u'Республика Дагестан'),
    (u'Кашин',u'Тверская область'),
    (u'Кемерово',u'Кемеровская область'),
    (u'Керчь',u'Крым'),
    (u'Кингисепп',u'Ленинградская область'),
    (u'Киров',u'Кировская область'),
    (u'Кирово-Чепецк',u'Кировская область'),
    (u'Кисловодск',u'Ставропольский край'),
    (u'Климовск',u'Московская область'),
    (u'Клин',u'Московская область'),
    (u'Коломна',u'Московская область'),
    (u'Комсомольск-на-Амуре',u'Хабаровский край'),
    (u'Кондрово',u'Калужская область'),
    (u'Королев',u'Московская область'),
    (u'Кострома',u'Костромская область'),
    (u'Котлас',u'Архангельская область'),
    (u'Красногорск',u'Московская область'),
    (u'Краснодар',u'Краснодарский край'),
    (u'Красноярск',u'Красноярский край'),
    (u'Крымск',u'Краснодарский край'),
    (u'Кубинка',u'Московская область'),
    (u'Кузнецк',u'Пензенская область'),
    (u'Курган',u'Курганская область'),
    (u'Курск',u'Курская область'),
    (u'Лабинск',u'Краснодарский край'),
    (u'Лесозаводск',u'Приморский край'),
    (u'Липецк',u'Липецкая область'),
    (u'Лобня',u'Московская область'),
    (u'Ломоносов',u'Ленинградская область'),
    (u'Лучегорск',u'Приморский край'),
    (u'Лучегорск',u'Приморский край'),
    (u'Люберцы',u'Московская область'),
    (u'Магнитогорск',u'Челябинская область'),
    (u'Малоярославец',u'Калужская область'),
    (u'Махачкала',u'Республика Дагестан'),
    (u'Минеральные воды',u'Ставропольский край'),
    (u'Мирный',u'Приморский край'),
    (u'Мурманск',u'Мурманская область'),
    (u'Муром',u'Владимирская область'),
    (u'Мытищи',u'Московская область'),
    (u'Набережные Челны',u'Республика Татарстан'),
    (u'Нальчик',u'Кабардино-Балкария'),
    (u'Наро-Фоминск',u'Московская область'),
    (u'Нахабино',u'Московская область'),
    (u'Находка',u'Приморский край'),
    (u'Нефтекамск',u'Башкортостан'),
    (u'Нефтеюганск',u'Ханты-Мансийский автономный округ—Югра'),
    (u'Нижневартовск',u'Ханты-Мансийский автономный округ—Югра'),
    (u'Нижнекамск',u'Республика Татарстан'),
    (u'Нижний Новгород',u'Нижегородская область'),
    (u'Нижний Тагил',u'Свердловская область'),
    (u'Новозыбков',u'Брянская область'),
    (u'Новокузнецк',u'Кемеровская область'),
    (u'Новороссийск',u'Краснодарский край'),
    (u'Новосибирск',u'Новосибирская область'),
    (u'Новотроицк',u'Оренбургская область'),
    (u'Ноябрьск',u'Ямало-Ненецкий автономный округ'),
    (u'Обнинск',u'Калужская область'),
    (u'Одинцово',u'Московская область'),
    (u'Ожерелье',u'Московская область'),
    (u'Омск',u'Омская область'),
    (u'Орел',u'Орловская область'),
    (u'Оренбург',u'Оренбургская область'),
    (u'Орехово-Зуево',u'Московская область'),
    (u'Орск',u'Оренбургская область'),
    (u'Партизанск',u'Приморский край'),
    (u'Пенза',u'Пензенская область'),
    (u'Переславль-Залесский',u'Ярославская область'),
    (u'Пермь',u'Пермский край'),
    (u'Петрозаводск',u'Республика Карелия'),
    (u'Петропавловск-Камчатский',u'Камчатский край'),
    (u'Плес',u'Волгоградская область'),
    (u'Подольск',u'Московская область'),
    (u'Приморско-Ахтарск',u'Краснодарский край'),
    (u'Прокопьевск',u'Кемеровская область'),
    (u'Псков',u'Псковская область'),
    (u'Пушкино',u'Московская область'),
    (u'Пятигорск',u'Ставропольский край'),
    (u'Раменское',u'Московская область'),
    (u'Ревда',u'Свердловская область'),
    (u'Ржев',u'Тверская область'),
    (u'Россошь',u'Воронежская область'),
    (u'Ростов-на-Дону',u'Ростовская область'),
    (u'Рузаевка',u'Мордовия'),
    (u'Рязань',u'Рязанская область'),
    (u'Саки',u'Крым'),
    (u'Салават',u'Республика Башкортостан'),
    (u'Самара',u'Самарская область'),
    (u'Саранск',u'Республика Мордовия'),
    (u'Саратов',u'Саратовская область'),
    (u'Саров',u'Нижегородская область'),
    (u'Северск',u'Томская область'),
    (u'Сергиев Посад',u'Московская область'),
    (u'Серпухов',u'Московская область'),
    (u'Сертолово',u'Ленинградская область'),
    (u'Сибай',u'Башкортостан'),
    (u'Симеиз',u'Крым'),
    (u'Симферополь',u'Крым'),
    (u'Славянск-на-Кубани',u'Краснодарский край'),
    (u'Смирных',u'Сахалинская область'),
    (u'Смоленск',u'Смоленская область'),
    (u'Солнечногорск',u'Московская область'),
    (u'Сосновоборск',u'Красноярский край'),
    (u'Сосновый Бор',u'Ленинградская область'),
    (u'Сочи',u'Краснодарский край'),
    (u'Спасск-Дальний',u'Приморский край'),
    (u'Ставрополь',u'Ставропольский край'),
    (u'Старый Крым',u'Крым'),
    (u'Старый Оскол',u'Белгородская область'),
    (u'Стерлитамак',u'Республика Башкортостан'),
    (u'Ступино',u'Московская область'),
    (u'Судак',u'Крым'),
    (u'Сургут',u'Ханты-Мансийский автономный округ—Югра'),
    (u'Сухиничи',u'Калужская область'),
    (u'Сызрань',u'Самарская область'),
    (u'Сыктывкар',u'Республика Коми'),
    (u'Сысерть',u'Свердловская область'),
    (u'Тавричанка',u'Приморский край'),
    (u'Таганрог',u'Ростовская область'),
    (u'Талдом',u'Московская область'),
    (u'Тамбов',u'Тамбовская область'),
    (u'Тверь',u'Тверская область'),
    (u'Темрюк',u'Краснодарский край'),
    (u'Тихвин',u'Ленинградская область'),
    (u'Тобольск',u'Тюменская область'),
    (u'Тольятти',u'Самарская область'),
    (u'Томск',u'Томская область'),
    (u'Туапсе',u'Краснодарский край'),
    (u'Тула',u'Тульская область'),
    (u'Тулун',u'Иркутская область'),
    (u'Тында',u'Амурская область'),
    (u'Тюмень',u'Тюменская область'),
    (u'Улан-Удэ',u'Республика Бурятия'),
    (u'Ульяновск',u'Ульяновская область'),
    (u'Урюпинск',u'Волгоградская область'),
    (u'Усолье-Сибирское',u'Иркутская область'),
    (u'Уссурийск',u'Приморский край'),
    (u'Уфа',u'Республика Башкортастан'),
    (u'Ухта',u'Республика Коми'),
    (u'Феодосия',u'Крым'),
    (u'Фокино',u'Приморский край'),
    (u'Хабаровск',u'Хабаровский край'),
    (u'Хороль',u'Приморский край'),
    (u'Хотьково',u'Московская область'),
    (u'Чайковский',u'Пермский край'),
    (u'Чебоксары',u'Чувашская Республика'),
    (u'Челябинск',u'Челябинская область'),
    (u'Череповец',u'Вологодская область'),
    (u'Черкесск',u'Карачаево-Черкесская Республика'),
    (u'Черноморское',u'Крым'),
    (u'Чита',u'Забайкальскй край'),
    (u'Шатура',u'Московская область'),
    (u'Шелехов',u'Иркутская область'),
    (u'Шлиссельбург',u'Ленинградская область'),
    (u'Щекино',u'Тульская область'),
    (u'Щелково',u'Московская область'),
    (u'Электросталь',u'Московская область'),
    (u'Энгельс',u'Саратовская область'),
    (u'Югорск',u'Ханты-Мансийский автономный округ—Югра'),
    (u'Южно-Сахалинск',u'Свердловская область'),
    (u'Юхнов',u'Калужская область'),
    (u'Якутск',u'Саха'),
    (u'Ялта',u'Крым'),
    (u'Ярославль',u'Ярославская область'),
    (u'Анадырь',u'Чукотский автономный округ'),
    (u'Белово',u'Кемеровская область'),
    (u'Белогорск',u'Амурская область'),
    (u'Бердск',u'Новосибирская область'),
    (u'Богданович',u'Свердловская область'),
    (u'Борисоглебск',u'Воронежская область'),
    (u'Ванино',u'Хабаровский край'),
    (u'Дальнегорск',u'Приморский край'),
    (u'Елец',u'Липецкая область'),
    (u'Завитинск',u'Амурская область'),
    (u'Звенигород',u'Московская область'),
    (u'Зеленогорск',u'Красноярский край'),
    (u'Зея',u'Амурская область'),
    (u'Змеиногорск',u'Алтайский край'),
    (u'Калачинск',u'Омская область'),
    (u'Каменка',u'Воронежская область'),
    (u'Камень-на-Оби',u'Алтайский край'),
    (u'Карасук',u'Новосибирская область'),
    (u'Кириши',u'Ленинградская область'),
    (u'Киселевск',u'Кемеровская область'),
    (u'Колпино',u'Санкт-Петербург'),
    (u'Красноуфимск',u'Свердловская область'),
    (u'Лазо',u'Камчатский край'),
    (u'Ленинск',u'Пензенская областьий'),
    (u'Магадан',u'Магаданская область'),
    (u'Михайловка',u'Волгоградская область'),
    (u'Надым',u'Ямало-Ненецкий автономный округ'),
    (u'Нерюнгри',u'Республика Саха (Якутия)'),
    (u'Николаевск-на-Амуре',u'Хабаровский край'),
    (u'Новоалтайск',u'Алтайский край'),
    (u'Новочебоксарск',u'Чувашия'),
    (u'Новочеркасск',u'Ростовская область'),
    (u'Облучье',u'Еврейская автономная область'),
    (u'Преображение',u'Приморский'),
    (u'Приморский',u'Приморский край'),
    (u'Райчихинск',u'Амурская область'),
    (u'Рассказово',u'Тамбовская область'),
    (u'Рубцовск',u'Алтайский край'),
    (u'Саяногорск',u'Хакасия'),
    (u'Саянск',u'Иркутская область'),
    (u'Свободный',u'Амурская область'),
    (u'Серышево-2',u'Амурская область'),
    (u'Сковородино',u'Амурская область'),
    (u'Советская Гавань',u'Хабаровский край'),
    (u'Тимашевск',u'Краснодарский край'),
    (u'Томмот',u'Якутия'),
    (u'Усть-Илимск',u'Иркутская область'),
    (u'Химки',u'Московская область'),
    (u'Черепаново',u'Новосибирская область'),
    (u'Шимановск',u'Амурская область'),
    (u'Юрга',u'Кемеровская область'),
    (u'Ялуторовск',u'Тюменская область')]