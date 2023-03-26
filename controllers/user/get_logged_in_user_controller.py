
async def get_logged_in_user_controller(request, response):

    # on success, send the current user to the client
    return {
        '_id': str(request.state.user['_id']),
        'username': request.state.user['username'],
        'csrf': request.state.user['csrf']
    }
