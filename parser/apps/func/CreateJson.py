class CreateJson:
    def __init__(self, text: str):
        """

        :type text: object
        """
        self.text = text

    def create_olx_apartment(self):
        file = open('apps/files/Olx_apartment.json', 'w')
        file.write(self.text[2:-1])
        file.close()

