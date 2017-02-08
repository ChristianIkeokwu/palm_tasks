from src.common import mail






credentials = mail.get_credentials()

service = mail.discovery.build('gmail', 'v1', http=credentials.authorize(mail.httplib2.Http()))
testMessage = mail.CreateMessage('christianthrone@gmail.com', 'christianikeokwu@gmail.com', 'Html testing',
                            message_html)
testSend = mail.SendMessage(service, 'me', testMessage)
