import boto3

class Aws:
    def send_file(self) -> None:
        #to-do
        #client = boto3.client('glacier', region_name='your-region')
        
        #vault_name = 'your-vault-name'
        
        #filename = 'path/to/yourfile.ext'
        
        #with open(filename, 'rb') as file:
        #    archive = client.upload_archive(vaultName=vault_name, body=file)
        return None

    def get_file(self) -> None:
        #to-do
        return None

    def move_file(self) -> None:
        #to-do
        return None

    def remove_file(self) -> None:
        #to-do
        # client = boto3.client('glacier', region_name='your-region')
        # vault_name = 'your-vault-name'
        # archive_id = 'your-archive-id'
        # response = client.delete_archive(vaultName=vault_name, archiveId=archive_id)
        # print(f"Archive {archive_id} deleted successfully")
        return None
