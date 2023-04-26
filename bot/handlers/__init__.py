"""
Register handlers
"""
from aiogram import Router, F
from aiogram.filters import CommandStart, Command

from bot.handlers.adv_search import (
    adv_search_main,
    adv_search_prof_role,
    adv_search_exp_type,
    adv_search_show_vacancies
)
from bot.handlers.basic_search import (
    vacancy_basic_search_main,
    switch_message_page_callback
)
from bot.handlers.help import help_command, help_func
from bot.handlers.profile_create import (
    profile_main,
    profile_create_firstname,
    profile_create_lastname,
    profile_create_email,
    profile_create_professional,
    profile_create_experience,
    profile_create_end,
)
from bot.handlers.profile_update import (
    profile_edit,
    profile_edit_choose_field,
    profile_partial_updater,
    next_step_handler,
    profile_partial_update_grade
)
from bot.handlers.start import start
from bot.structure import (
    SearchCallBack,
    ProfileCallBack,
    ProfileCreateStates,
    FieldTypeToUpdateCallBack,
    ProfileUpdateStates,
    NextStepCallBack,
    ExpTypeCallBack,
    AdvSearchStates,
)
from bot.text_for_messages import BOT_COMMANDS_INFO

__all__ = [
    "BOT_COMMANDS_INFO",
    "register_user_commands",
]


# from bot.middleware import RegisterCheck


def register_user_commands(router: Router) -> None:
    """
    Register user commands
    :param router: 
    :return: 
    """
    # middleware
    # router.message.middleware(RegisterCheck())
    # router.callback_query.middleware(RegisterCheck())
    router.message.register(start, CommandStart())

    # help
    router.message.register(help_command, Command(commands=["help"]))
    router.message.register(help_func, F.text == "Помощь")

    # profile main
    router.message.register(profile_main, Command(commands=["profile"]))
    router.message.register(profile_main, F.text == "Профиль")

    # profile editing
    router.callback_query.register(
        profile_edit,
        ProfileCallBack.filter(),
        ProfileUpdateStates.waiting_for_choose_edit_type
    )
    router.callback_query.register(
        profile_edit_choose_field,
        FieldTypeToUpdateCallBack.filter(),
        ProfileUpdateStates.waiting_for_choose_field,
    )
    router.message.register(
        profile_partial_updater,
        ProfileUpdateStates.waiting_for_partial_update_data,
    )
    router.callback_query.register(
        profile_partial_update_grade,
        ExpTypeCallBack.filter(),
        ProfileUpdateStates.waiting_for_partial_update_data,
    )

    router.callback_query.register(
        next_step_handler,
        NextStepCallBack.filter(),
        ProfileUpdateStates.waiting_for_next_step,
    )

    # profile creating
    router.callback_query.register(
        profile_create_firstname,
        ProfileCallBack.filter(),
        ProfileCreateStates.waiting_for_choose_create_type
    )
    router.message.register(profile_create_lastname, ProfileCreateStates.waiting_for_firstname)
    router.message.register(profile_create_email, ProfileCreateStates.waiting_for_lastname)
    router.message.register(profile_create_professional, ProfileCreateStates.waiting_for_email)
    router.message.register(profile_create_experience, ProfileCreateStates.waiting_for_professional_role)
    router.callback_query.register(
        profile_create_end,
        ExpTypeCallBack.filter(),
        ProfileCreateStates.waiting_for_experience
    )

    # search
    router.message.register(vacancy_basic_search_main, Command(commands=["search"]))
    router.message.register(vacancy_basic_search_main, F.text == "Поиск по вакансиям")
    router.callback_query.register(switch_message_page_callback, SearchCallBack.filter())

    # adv search
    router.message.register(adv_search_main, Command(commands=["adv_search"]))
    router.message.register(adv_search_main, F.text == "Расширенный поиск")
    router.message.register(adv_search_prof_role, AdvSearchStates.waiting_for_prof_role)
    router.callback_query.register(
        adv_search_exp_type,
        ExpTypeCallBack.filter(),
        AdvSearchStates.waiting_for_exp)
    router.message.register(adv_search_show_vacancies, AdvSearchStates.waiting_for_number_of_vacancies)

    router.callback_query.register(switch_message_page_callback, SearchCallBack.filter())
