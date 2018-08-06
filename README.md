# Anna.Task

TODO
* Хостинг статики нужно перенести в nginx/s3/...
* Процесс индексации HackerNews нужно вынести в отдельный процесс
* Индексация сделано топорно. Нужно либо перенести на ElasticSearch, либо подойти основательно к алгоритму
* Нужны тесты. Особенно на индексацию
* Инициализация ClientSession выдаёт предупреждение. Нужно придумать как избавиться от предупреждения, но оставить ClientSession единственным экземпляромдля приложения.
* Хранение состояния индексера на диске в папке приложения — так себе затея. От неё нужно избавляться. Это должен быть или Эластик, если мы его прикручиваем, или какой-нибудь redis/mongodb. Это нам, кстати, в будущем позволит горизонтально масштабироваться.
* Состояние индексера после загрузки с диска нужно валидировать
* Клиентская часть сделана на коленке. Там бы прикрутить webpack, ts, react, ...
* Firebase Admin SDK для Python, судя по документации, не поддерживает уведомления об изменениях, и все равно нужно было бы писать явный polling. Поэтому я решил от него отказаться. Но в будущем, возможно, стоит использовать его.
* Я сознательно допускаю, что запись состояния индексера на диск не гарантировано. Мне кажется, это хороший компромис нагрузки на файловую систему и надежности. В худшем случаем мы потерям несколько секунд работы и восстановим их после запуска.