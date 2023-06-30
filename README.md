# SteamMarket

Этот репозиторий содержит python-скрипт для формирования csv-файла по данным из excel-файла с предметами на торговой площадке Steam

## Использование steam_market.ipynb

Запишите в "items.xlsx" названия и категории предметов, по которым нужны данные с торговой площадки Steam. Файл "items.xlsx" должен находиться в директории, в которой запущен Jupyter Notebook. Далее необходимо авторизоваться на сайте [https://store.steampowered.com](https://steamcommunity.com). После этого нажмите правой кнопкой мыши на любом месте на странице [https://store.steampowered.com](https://steamcommunity.com) и выберите "Посмотреть код элемента" в контекстном меню. Это откроет инструменты разработчика или панель инспектора элементов браузера. В открывшейся панели инструментов разработчика найдите вкладку "Application". В левой панели раздела "Application" раскройте пункт "Storage" и выберите "Cookies". В "Cookies" найдите "steamLoginSecure", "sessionid", "browserid" и добавьте их значения в файл "steam_market.ipynb" в переменные "steam_login_secure", "session_id" и "browser_id" соответственно. Далее запустите скрипт "steam_market.ipynb" в результате чего в директории, в которой запущен Jupyter Notebook появится файл "items.csv". В дальнейшем его можно использовать для построения визуализаций. Например, в [Tableau](https://public.tableau.com/app/profile/ilya.pushin/viz/CSGOSteamMarket/CSGO).

## Использование steam_market_unauthorized.ipynb
Запишите в "items.xlsx" названия и категории предметов, по которым нужны данные с торговой площадки Steam. Файл "items.xlsx" должен находиться в директории, в которой запущен Jupyter Notebook. Далее запустите скрипт "steam_market_unauthorized.ipynb" в результате чего в директории, в которой запущен Jupyter Notebook появится файл "items.csv". В дальнейшем его можно использовать для построения визуализаций. Например, в [Tableau](https://public.tableau.com/app/profile/ilya.pushin/viz/CSGOSteamMarket/CSGO). Отличие "steam_market_unauthorized.ipynb" от "steam_market.ipynb" в том, что без авторизации цена продажи предмета будет в долларах, а не в валюте аккаунта.

### Используемые технологии

- Python

## Примечание
В скриптах "steam_market.ipynb" и "steam_market_unauthorized.ipynb" можно выбрать игру по которой нужны данные с торговой площадки Steam. В переменной game_id - укажите steam id игры. Найти steam id можно в url, например, [https://store.steampowered.com/app/730/CounterStrike_Global_Offensive](https://store.steampowered.com/app/730/CounterStrike_Global_Offensive) у CS GO steam id 730.

### Автор

Пушин Илья
