from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.data.redis.queries import RedisQueries
from bot.mics.text_formatting import format_text
from bot.ui.res.strings import Strings
from bot.ui.keyboards.inline_markups import NewPublicationSectionMarkups
from bot.ui.states.state_machine import NewPublicationStates


router = Router()


@router.message(NewPublicationStates.publication_title)
async def publication_title_entry(message: Message, state: FSMContext, redis: RedisQueries) -> None:
    """
    Обрабатывает ввод заголовка публикации.
    Автоматически заголовок оборачивается в жирный курсив.
    :param message:
    :param state:
    :param redis:
    :return:
    """
    model = await redis.get_new_publication()
    model.publication_title = format_text(message, bolditalic=True)
    await redis.save_new_publication(model)

    await message.answer(Strings.publication_text, reply_markup=NewPublicationSectionMarkups.publication_text())
    await state.set_state(NewPublicationStates.publication_text)


@router.message(NewPublicationStates.publication_text)
async def publication_text_entry(message: Message, state: FSMContext, redis: RedisQueries) -> None:
    """
    Третий - это текст публикации.
    Пользователь отправляет текст, а после может редактировать его.
    :param message:
    :param state:
    :param redis:
    :return:
    """
    model = await redis.get_new_publication()
    model.publication_text = format_text(message)
    model.message_id = message.message_id
    await redis.save_new_publication(model)

    await message.answer(
        Strings.editing_publication_text,
        reply_markup=NewPublicationSectionMarkups.editing_publication_text())
    await state.set_state(NewPublicationStates.editing_publication_text)


@router.edited_message(NewPublicationStates.editing_publication_text)
async def editing_publication_text_entry(message: Message, redis: RedisQueries) -> None:
    """
    Обрабатывает изменение сообщения, отправленного только на предыдущем шаге.
    :param message:
    :param redis:
    :return:
    """
    model = await redis.get_new_publication()
    if message.message_id != model.message_id:
        return

    model.publication_text = format_text(message)
    await redis.save_new_publication(model)
