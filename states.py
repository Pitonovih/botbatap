from aiogram.dispatcher.filters.state import State, StatesGroup

class UploadState(StatesGroup):
    """Состояния для загрузки файлов"""
    waiting_for_file = State()

class PasswordState(StatesGroup):
    """Состояния для работы с паролями"""
    waiting_password_set = State()    
    waiting_password_input = State()  
