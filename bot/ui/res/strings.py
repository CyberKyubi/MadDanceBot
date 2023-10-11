from .emoji import Emoji


class Strings:
    main_menu = f"{Emoji.house} Главное меню <b>MadDanceBot</b>"

    publication_date = (f"{Emoji.clock9} Укажи дату публикации в формате <i><b>20.09</b></i>\n\n"
                        "Для удобства воспользуйся <i>\"Горячими кнопками\"</i>")
    publication_time = (f"{Emoji.clock330} Укажи время публикации в формате <i><b>17.00</b></i>\n\n"
                        "Для удобства воспользуйся <i>\"Горячими кнопками\"</i>")
    publication_title = f"{Emoji.pushpin} Заголовок публикации:"
    publication_text = f"{Emoji.book} Текст публикации:"
    editing_publication_text = (f"{Emoji.pencil2} Как завершишь редактирование текста,\n"
                                f"нажми <b>\"Запланировать\"</b> ")
    publication_canceled = f"{Emoji.x} Заполнение новой публикации было отменено"
    publication_info = (f"{Emoji.book} Публикация запланирована:\n\n"
                        "{title}\n"
                        "{publication_date}")

    section_of_scheduled_publication = f"{Emoji.calendar} Раздел <b><i>\"Запланированные публикации\"</i></b>\n\n\n"
    list_of_upcoming_publications = (f"{Emoji.book} Будущие:\n\n"  # 
                                     "{}\n")
    list_of_overdue_publications = (f"{Emoji.exclamation} Просроченные:\n\n"  # {Emoji.exclamation}
                                    "{}\n\n")
    elem_of_list_of_publications = ("{roman_num}.  {publication_title}\n"
                                    "{publication_at}\n\n")
    no_upcoming_publications = f"{Emoji.book} Ближайших публикаций нет."

    month_gap = "Даты публикаций разделены по месяцам, выбери нужный месяц:"
    week_range = "Даты публикаций разбиты на недели, выбери нужную неделю:"

    publication_page = ("{title}\n\n"
                        "{text}\n\n"
                        "<b>———✂️———</b>\n\n"
                        "Дата публикации:\n"
                        "{date}")


class Errors:
    invalid_date_format = "Неверный формат даты"
    invalid_time_format = "Неверный формат времени"
    past_publication_time_error = "Время публикации не может быть прошедшим!"

