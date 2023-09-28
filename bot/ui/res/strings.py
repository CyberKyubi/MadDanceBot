from .emoji import Emoji


class Strings:
    main_menu = (f"{Emoji.house} Главное меню <b>MadDanceBot</b>\n\n"
                 f"{Emoji.book} Ближайших публикаций нет.")

    publication_date = (f"{Emoji.clock9} Укажи дату публикации в формате <i><b>20.09</b></i>\n\n"
                        "Для удобства воспользуйся <i>\"Горячими кнопками\"</i>")
    publication_time = (f"{Emoji.clock330} Укажи время публикации в формате <i><b>17.00</b></i>\n\n"
                        "Для удобства воспользуйся <i>\"Горячими кнопками\"</i>")
    publication_title = f"{Emoji.pushpin} Заголовок публикации:"
    publication_text = f"{Emoji.book} Текст публикации:"
    editing_publication_text = (f"{Emoji.pencil2} Как завершишь редактирование текста,\n"
                                f"нажми <b>\"Запланировать\"</b> ")
    publication_canceled = f"{Emoji.x} Заполнение новой публикации было отменено"
    publication_info = (f"{Emoji.book} Публикация запланирована:\n"
                        "Дата и время: <i><b>{datetime}</b></i>")


class Errors:
    invalid_date_format = "Неверный формат даты"
    invalid_time_format = "Неверный формат времени"
    past_publication_time_error = "Время публикации не может быть прошедшим!"

