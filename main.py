import flet as ft 

import google.generativeai as genai 

genai.configure(api_key='AIzaSyDT9qAoNzOCCSW4TGNnn-n2FeCNAIf8xLA')
model = genai.GenerativeModel('gemini-pro')

def display_message(chat_container,role,message_text):
    if role == 'user':
        role_color = ft.colors.GREEN_300
        role_text = 'You'
    else:
        role_color = ft.colors.BLUE_300
        role_text = 'Gemini'
    message_area = ft.SelectionArea(
        content=ft.Column([
        ft.Text(role_text,weight='bold',color=role_color),
        ft.Text(message_text)
        ])
    )
    chat_container.controls.append(message_area)

def update_chat(page,chat_container,chat , prompt):
    display_message(chat_container,'user',prompt)
    response = chat.send_message(prompt)
    display_message(chat_container,'bot',response.parts[0].text)
    page.update()

def main(page:ft.Page):
    page.title='Gemini Chat'
    page.window.width = 400
    page.window.height = 750

    if not hasattr(page,'chat'):
        page.chat = model.start_chat(history=[])
        
    user_input= ft.TextField(hint_text="ماذا نريد ؟",expand=True)
    chat_container = ft.Column(scroll='always',expand=True,auto_scroll=True)
    def send_message(e):
        if user_input.value.strip() != "":
            update_chat(page,chat_container,page.chat,user_input.value)
            user_input.value= ''
            page.update()
    send_button= ft.ElevatedButton(text='Send',on_click=send_message) 
    page.add(
        chat_container,
        ft.Row([
        user_input,
        send_button
        ])
    )       
ft.app(target=main,assets_dir='assets/')    