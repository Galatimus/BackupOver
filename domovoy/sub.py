#!/usr/bin/python
# -*- coding: utf-8 -*-

conv =[(u'Александров',u'Владимирская область'),
       (u'Альметьевск',u'Татарстан'),
       (u'Анапа',u'Краснодарский край'),
       (u'Ангарск',u'Иркутская область'),
       (u'Арзамас',u'Нижегородская область'),
       (u'Архангельск',u'Архангельская область'),
       (u'Северодвинск',u'Архангельская область'),
       (u'Астрахань',u'Астраханская область'),
       (u'Балаково',u'Саратовская область'),
       (u'Балашиха',u'Московская область'),
       (u'Барнаул',u'Алтайский край'),
       (u'Белгород',u'Белгородская область'),
       (u'Белорецк',u'Башкортостан'),
       (u'Бийск',u'Алтайский край'),
       (u'Благовещенск',u'Амурская область'),
       (u'Богородск',u'Нижегородская область'),
       (u'Боровичи',u'Новгородская область'),
       (u'Братск',u'Иркутская область'),
       (u'Бронницы',u'Московская область'),
       (u'Брянск',u'Брянская область'),
       (u'Великие Луки',u'Псковская область'),
       (u'Великий Новгород',u'Новгородская область'),
       (u'Видное',u'Московская область'),
       (u'Владивосток',u'Приморский край'),
       (u'Владикавказ',u'Республика Северная Осетия-Алания'),
       (u'Владимир',u'Владимирская область'),
       (u'Волгоград',u'Волгоградская область'),
       (u'Волгодонск',u'Ростовская область'),
       (u'Волжский',u'Волгоградская область'),
       (u'Вологда',u'Вологодская область'),
       (u'Грязовец',u'Вологодская область'),
       (u'Воронеж',u'Воронежская область'),
       (u'Выкса',u'Нижегородская область'),
       (u'Вязники',u'Владимирская область'),
       (u'Грозный',u'Чеченская Республика'),
       (u'Домодедово',u'Московская область'),
       (u'Екатеринбург',u'Свердловская область'),
       (u'Ессентуки',u'Ставропольский край'),
       (u'Железнодорожный',u'Московская область'),
       (u'Жуковский',u'Московская область'),
       (u'Зеленоград',u'Москва'),
       (u'Златоуст',u'Челябинская область'),
       (u'Иваново',u'Ивановская область'),
       (u'Кохма',u'Ивановская область'),
       (u'Ижевск',u'Удмуртская республика'),
       (u'Иркутск',u'Иркутская область'),
       (u'Истра',u'Московская область'),
       (u'Йошкар-Ола',u'Республика Марий Эл'),
       (u'Казань',u'Республика Татарстан'),
       (u'Калач-на-Дону',u'Волгоградская область'),
       (u'Калининград',u'Калининградская область'),
       (u'Калуга',u'Калужская область'),
       (u'Каменск-Уральский',u'Свердловская область'),
       (u'Каменск-Шахтинский',u'Ростовская область'),
       (u'Камышин',u'Волгоградская область'),
       (u'Кемерово',u'Кемеровская область'),
       (u'Киров',u'Кировская область'),
       (u'Кирово-Чепецк',u'Кировская область'),
       (u'Кисловодск',u'Ставропольский край'),
       (u'Климовск',u'Московская область'),
       (u'Клин',u'Московская область'),
       (u'Коломна',u'Московская область'),
       (u'Комсомольск-на-Амуре',u'Хабаровский край'),
       (u'Королев',u'Московская область'),
       (u'Кострома',u'Костромская область'),
       (u'Котлас',u'Архангельская область'),
       (u'Красногорск',u'Московская область'),
       (u'Краснодар',u'Краснодарский край'),
       (u'Красноярск',u'Красноярский край'),
       (u'Кузнецк',u'Пензенская область'),
       (u'Курган',u'Курганская область'),
       (u'Курск',u'Курская область'),
       (u'Липецк',u'Липецкая область'),
       (u'Лобня',u'Московская область'),
       (u'Магнитогорск',u'Челябинская область'),
       (u'Махачкала',u'Республика Дагестан'),
       (u'Минеральные воды',u'Ставропольский край'),
       (u'Мурманск',u'Мурманская область'),
       (u'Муром',u'Владимирская область'),
       (u'Мытищи',u'Московская область'),
       (u'Набережные Челны',u'Республика Татарстан'),
       (u'Нальчик',u'Кабардино-Балкария'),
       (u'Нахабино',u'Московская область'),
       (u'Находка',u'Приморский край'),
       (u'Нефтекамск',u'Башкортостан'),
       (u'Нефтеюганск',u'Ханты-Мансийский автономный округ—Югра'),
       (u'Нижневартовск',u'Ханты-Мансийский автономный округ—Югра'),
       (u'Нижнекамск',u'Республика Татарстан'),
       (u'Нижний Новгород',u'Нижегородская область'),
       (u'Нижний Тагил',u'Свердловская область'),
       (u'Новокузнецк',u'Кемеровская область'),
       (u'Новороссийск',u'Краснодарский край'),
       (u'Новосибирск',u'Новосибирская область'),
       (u'Новотроицк',u'Оренбургская область'),
       (u'Ноябрьск',u'Ямало-Ненецкий автономный округ'),
       (u'Обнинск',u'Калужская область'),
       (u'Одинцово',u'Московская область'),
       (u'Омск',u'Омская область'),
       (u'Орел',u'Орловская область'),
       (u'Оренбург',u'Оренбургская область'),
       (u'Орск',u'Оренбургская область'),
       (u'Пенза',u'Пензенская область'),
       (u'Пермь',u'Пермский край'),
       (u'Петрозаводск',u'Республика Карелия'),
       (u'Петропавловск-Камчатский',u''),
       (u'Подольск',u'Московская область'),
       (u'Прокопьевск',u'Кемеровская область'),
       (u'Псков',u'Псковская область'),
       (u'Пушкино',u'Московская область'),
       (u'Пятигорск',u'Ставропольский край'),
       (u'Ревда',u'Свердловская область'),
       (u'Россошь',u'Воронежская область'),
       (u'Ростов-на-Дону',u'Ростовская область'),
       (u'Рузаевка',u'Мордовия'),
       (u'Рязань',u'Рязанская область'),
       (u'Салават',u'Республика Башкортостан'),
       (u'Самара',u'Самарская область'),
       (u'Саранск',u'Республика Мордовия'),
       (u'Саратов',u'Саратовская область'),
       (u'Саров',u'Нижегородская область'),
       (u'Северск',u'Томская область'),
       (u'Сергиев Посад',u'Московская область'),
       (u'Серпухов',u'Московская область'),
       (u'Симферополь',u'Крым'),
       (u'Смоленск',u'Смоленская область'),
       (u'Сочи',u'Краснодарский край'),
       (u'Ставрополь',u'Ставропольский край'),
       (u'Старый Оскол',u'Белгородская область'),
       (u'Стерлитамак',u'Республика Башкортостан'),
       (u'Сургут',u'Ханты-Мансийский автономный округ—Югра'),
       (u'Сызрань',u'Самарская область'),
       (u'Сыктывкар',u'Республика Коми'),
       (u'Таганрог',u'Ростовская область'),
       (u'Тамбов',u'Тамбовская область'),
       (u'Тверь',u'Тверская область'),
       (u'Тобольск',u'Тюменская область'),
       (u'Тольятти',u'Самарская область'),
       (u'Томск',u'Томская область'),
       (u'Туапсе',u'Краснодарский край'),
       (u'Тула',u'Тульская область'),
       (u'Тюмень',u'Тюменская область'),
       (u'Улан-Удэ',u'Республика Бурятия'),
       (u'Ульяновск',u'Ульяновская область'),
       (u'Урюпинск',u'Волгоградская область'),
       (u'Уссурийск',u'Приморский край'),
       (u'Уфа',u'Республика Башкортастан'),
       (u'Ухта',u'Республика Коми'),
       (u'Феодосия',u'Крым'),
       (u'Петропавловск-Камчатский',u'Камчатский край'),
       (u'Хабаровск',u'Хабаровский край'),
       (u'Хотьково',u'Московская область'),
       (u'Чебоксары',u'Чувашская Республика'),
       (u'Челябинск',u'Челябинская область'),
       (u'Череповец',u'Вологодская область'),
       (u'Сокол',u'Вологодская область'),
       (u'Шексна',u'Вологодская область'),
       (u'Вытегра',u'Вологодская область'),
       (u'Тотьма',u'Вологодская область'),
       (u'с. Липин Бор',u'Вологодская область'),
       (u'Черкесск',u'Карачаево-Черкесская Республика'),
       (u'Чита',u'Забайкальскй край'),
       (u'Щелково',u'Московская область'),
       (u'Электросталь',u'Московская область'),
       (u'Рыбинск',u'Ярославская область'),
       (u'Энгельс',u'Саратовская область'),
       (u'Югорск',u'Ханты-Мансийский автономный округ—Югра'),
       (u'Южно-Сахалинск',u'Свердловская область'),
       (u'Якутск',u'Саха'),
       (u'Ялта',u'Крым'),
       (u'Ярославль',u'Ярославская область')] 