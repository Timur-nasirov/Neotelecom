from aiogram import Dispatcher, Bot, executor, types
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import TOKEN
from parser import parsing
from logging import basicConfig, INFO

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
basicConfig(level=INFO)

class SaveID:
	def __init__(self):
		self.id_ = ''
	def read(self):
		return self.id_
	def write(self, name):
		self.id_ = name
saveid = SaveID()

class IdState(StatesGroup):
	id_ = State()

class NameState(StatesGroup):
	name = State()

class SignState(StatesGroup):
	login = State()
	password = State()

@dp.message_handler(commands='start')
async def start(message: types.Message):
	await message.answer('/task - проверить невыполненные задания\n/sign - войти\n/exit - выйти')

@dp.message_handler(commands='exit')
async def exit(message:types.Message):
	if saveid.read() == '':
		await message.answer('Вы еще не вошли!')
	else:
		saveid.write('')
		await message.answer('Успешно!')

@dp.message_handler(commands='sign')
async def sign_login(message: types.Message):
	await message.answer('Введите логин:')
	await SignState.login.set()

@dp.message_handler(state=SignState.login)
async def sign_pass(message: types.Message, state: FSMContext):
	await state.update_data(login=message.text)
	await message.answer('Введите пароль:')
	await SignState.password.set()

@dp.message_handler(state=SignState.password)
async def sign_end(message: types.Message, state: FSMContext):
	await state.update_data(password=message.text)
	data = await storage.get_data(user=message.from_user.id)
	await state.finish()
	pars = parsing([data['login'], data['password']], 'sign')
	if pars == 'none':
		await message.answer('Неверный логин или пароль!')
	else:
		saveid.write(pars)
		count = parsing(saveid.read(), 'count')

		await message.answer(f'Здравствуйте, {parsing(pars, "names")}\n/task - проверить невыполненные задания')

@dp.message_handler(commands='task')
async def check_count(message: types.message):
	if saveid.read() == '':
		await message.answer('Сначала войдите!')
	else:
		name = parsing(saveid.read(), 'names')
		count = parsing(saveid.read(), 'count')
		await message.answer(f'У вас не выполнено {count} заданий')

executor.start_polling(dp)