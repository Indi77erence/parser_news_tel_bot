# Токен бота.
BOT_TOKEN = ""
# Куда размещать посты
channels_id = ""

# Прокси
proxy = ["IP:PORT:LOGIN:PASS"]

# По каким дням парсить, все дни = *
work_days = ["monday", "tuesday", "wednesday", "thursday", "griday", "saturday", "sunday"]

# Время включения-выключения парсера (+3GTM)
work_start_time = "08:00"
work_end_time = "23:59"

# Время работы (3GTM), выключить функцию "off"
work_time = ["09:00", "10:00", "11:00"]

# Периодичность парсинга в минутах, выключить функцию "off" — функции work_time и work_period взаимоисключающие,
# работает или одна или вторая
work_period = 1

# url источника
URL = ["https://forklog.com/tag/uniswap", "https://forklog.com/tag/ethereum", "https://forklog.com/tag/bitcoin"]

# Хэштеги указываются над постом, выключить функцию "off"
hashtag = "on"

# Подпись - произвольный текст внизу поста
under_text = "Подробная информация на сайте"

# Длина поста указывается в знаках с пробелами - рекомендуется указывать от 400 до 1000, по умолчанию *,
text_length = 1000
