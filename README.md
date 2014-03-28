learn.csv - обучающая выборка 
userfilt.csv - тестовая выборка

обучить и протестировать:
python lrmgd.py learn.csv userfilt.csv

получить информацию из vkontakte:
python vk.py
Результат можно найти в users.csv
При желании можно отфильтровать его функцией all_valid('users.csv', 'usersfilt.csv') из файла filter.py
Фильтер оставляет лишь тех, у кого доступна вся нужная информция