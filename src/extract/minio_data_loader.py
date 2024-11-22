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
        json_content_list = []

        buckets = minio_client.list_buckets()
        for bucket in buckets:
            objects = minio_client.list_objects(bucket.name, recursive=True)
            for obj in objects:
                if obj.object_name.endswith('.json'):
                    response = minio_client.get_object(bucket.name, obj.object_name)

                    json_string = response.read().decode('utf-8')

                    try:
                        json_data = json.loads(json_string)
                        json_content_list.append(json_data)
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON from file {obj.object_name}: {e}")

        return json_content_list