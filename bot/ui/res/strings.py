from .emoji import Emoji


class Strings:
    main_menu = "главное меню"

    publication_date = ("Напиши дату публикации в формате <b>20.09</b>\n"
                        "Для ближайшего времени используй <i>Hot Buttons</i>")
    publication_time = ("Напиши время публикации в формате <b>17.0(0)</b>\n"
                        "Для ближайшего времени используй <i>Hot Buttons</i>")
    publication_text = f"{Emoji.book} Пришли текст публикации:"


class Errors:
    invalid_date_format = "Неверный формат даты"
    invalid_time_format = "Неверный формат времени"

