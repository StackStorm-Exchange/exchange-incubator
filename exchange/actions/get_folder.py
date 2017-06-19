from lib import BaseExchangeAction


class GetFolderAction(BaseExchangeAction):
    def run(self, folder_name):
        result = self.account.root.get_folder_by_name(name)

        return result
