
async def circular1(message, state, hidden_code):
    from user.user.handlers_for_finding import movie_from_code_code
    await movie_from_code_code(message, state, code=hidden_code)


async def circular2(message, state, user=None, delete=True):
    from main import start_command
    if user is None:
        user = message.from_user
    await start_command(message=message, state=state, user=user, delete=delete)
