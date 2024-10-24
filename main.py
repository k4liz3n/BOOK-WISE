import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes
from telegram.ext import filters

TOKEN = 'TOKEN-TELEGRAM'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hola! Envíame el título de un libro para obtener enlaces de compra y reseñas.')

async def get_book_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Mensaje recibido:", update.message.text)

    # Usar el texto completo del mensaje como consulta
    query = update.message.text.strip()  # Eliminar espacios innecesarios

    # Realiza la solicitud a la API de Google Books
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'items' in data:
            # Obtiene el primer libro de los resultados
            book = data['items'][0]  
            title = book['volumeInfo'].get('title', 'Sin título')
            authors = book['volumeInfo'].get('authors', ['Autor desconocido'])
            buy_link = book['volumeInfo'].get('infoLink', 'No disponible')
            description = book['volumeInfo'].get('description', 'No disponible')
            image_link = book['volumeInfo'].get('imageLinks', {}).get('thumbnail', 'No disponible')  # Enlace a la imagen

            # Crea un mensaje con todos los detalles
            message = f'Título: {title}\n' \
                      f'Autor(es): {", ".join(authors)}\n' \
                      f'Enlace de compra: {buy_link}\n' \
                      f'Descripción: {description[:200]}...'  # Solo muestra los primeros 200 caracteres
            
            # Envía el mensaje con la imagen
            await update.message.reply_photo(photo=image_link, caption=message)
        else:
            await update.message.reply_text('No se encontraron libros para esa búsqueda. Intenta con otro título.')
    else:
        await update.message.reply_text('Error al buscar información del libro. Intenta de nuevo más tarde.')

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_book_info))  # Evita que los comandos se procesen aquí
    
    app.run_polling()

if __name__ == '__main__':
    main()
