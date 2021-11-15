# arithmetic-mean-multiagents

## Зависимости
* spade -- Smart Python Agent Development Environment (>= 3.2.0)

## Добавление агентов
Согласно [документации](https://spade-mas.readthedocs.io/en/latest/usage.html#quick-start) spade вы должны зарегистрировать агентов на XMPP-сервере
* Например, на [404.city](https://404.city/#registration).

## Оценки алгоритма
| Память        | Обмен сообщениями   | Сообщение в центр  | 
| ------------- |:-------------:      | -----:             |
| O(1)          | O(n*n)              |   O(1)             |

## Запуск кода
### Создаем виртуальное окружение
```shell
python3 -m venv venv && source venv/bin/activate
```
### Установка зависимостей
```shell
pip3 install -r requirements.txt
```
### Запускаем 
```shell
python3 main.py
```