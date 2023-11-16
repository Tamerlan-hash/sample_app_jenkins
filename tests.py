import pytest

from unittest.mock import Mock, patch, AsyncMock

from telegram import Update, Message, Chat
from telegram.ext import CallbackContext
from main import new_meeting


class TestUnit:
    @pytest.mark.asyncio
    @patch('main.requests.post')
    async def test_new_meeting_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'webLink': 'https://example.com/meeting_link'
        }

        update = Mock(spec=Update)
        context = Mock(spec=CallbackContext)
        update.message = Mock(spec=Message)
        update.message.chat = Mock(spec=Chat)
        update.message.chat.id = 123456
        update.message.reply_text = AsyncMock()

        await new_meeting(update, context)

        update.message.reply_text.assert_awaited_with(
            'Ссылка на вашу видеоконференцию: https://example.com/meeting_link'
        )


    @pytest.mark.asyncio
    @patch('main.requests.post')
    async def test_new_meeting_failure(self, mock_post):
        mock_post.return_value.status_code = 400
        update = Mock(spec=Update)
        context = Mock(spec=CallbackContext)
        update.message = Mock(spec=Message)
        update.message.chat = Mock(spec=Chat)
        update.message.chat.id = 123456
        update.message.reply_text = AsyncMock()

        await new_meeting(update, context)

        update.message.reply_text.assert_awaited_with(
            'Произошла ошибка при создании видеоконференции.'
        )
