import re

def get_download_link(gdrive_url: str, only_file_id=None) -> str:
    """
    Преобразует стандартную ссылку Google Drive в прямую ссылку для скачивания.

    Принимает ссылки форматов:
    - drive.google.com
    - docs.google.com
    - drive.google.com

    Возвращает прямую ссылку для скачивания.
    """
    # Регулярное выражение для извлечения ID файла из разных форматов ссылок
    file_id_match = re.search(r'file/d/([a-zA-Z0-9_-]+)', gdrive_url)
    
    if file_id_match:
        file_id = file_id_match.group(1)

        if only_file_id:
            download_url = file_id
        else:              
            # Формат прямой ссылки для скачивания       
            download_url = f'https://drive.google.com/uc?export=view&id={file_id}&confirm=t'
        
        return download_url
    else:
        # Если ID не найден, возможно, ссылка имеет другой формат (например, общая папка),
        # либо не является ссылкой Google Drive.
        return "Ошибка: Не удалось найти ID файла в предоставленной ссылке."

# Пример использования внутри модуля для тестирования
if __name__ == "__main__":
    test_url = "drive.google.com"
    direct_link = get_download_link(test_url)
    print(f"Оригинальная ссылка: {test_url}")
    print(f"Ссылка для скачивания: {direct_link}")

