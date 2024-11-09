import json

from minio import Minio


class MinioDataLoader:
    def load_data_from_s3(self, addr: str, admin: str, password: str):
        minio_client = Minio(
            addr,
            access_key=admin,
            secret_key=password,
            secure=False  
        )
        # Список для сбора данных
        json_content_list = []

        buckets = minio_client.list_buckets()
        for bucket in buckets:
            objects = minio_client.list_objects(bucket.name, recursive=True)
            for obj in objects:
                # Проверяем, является ли файл JSON
                if obj.object_name.endswith('.json'):
                    # Получение объекта
                    response = minio_client.get_object(bucket.name, obj.object_name)

                    # Чтение содержимого объекта
                    json_string = response.read().decode('utf-8')  # Преобразуем байты в строку

                    # Парсинг JSON
                    try:
                        json_data = json.loads(json_string)  # Преобразуем строку в объект Python (словарь)
                        json_content_list.append(json_data)  # Добавляем содержимое в общий список
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON from file {obj.object_name}: {e}")

        return json_content_list