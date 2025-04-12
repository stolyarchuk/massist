from typing import Any, Dict, Union

from aiogram.filters import BaseFilter
from aiogram.types import Message


class HasUsernames(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        # Если entities вообще нет, вернётся None,
        # в этом случае считаем, что это пустой список
        entities = message.entities or []
        message_text = message.text or ""

        # Проверяем любые юзернеймы и извлекаем их из текста
        # методом extract_from(). Подробнее см. главу
        # про работу с сообщениями
        found_usernames = [
            item.extract_from(message_text) for item in entities
            if item.type == "mention"
        ]

        # Если юзернеймы есть, то "проталкиваем" их в хэндлер
        # по имени "usernames"
        if len(found_usernames) > 0:
            return {"usernames": found_usernames}
        # Если не нашли ни одного юзернейма, вернём False
        return False
