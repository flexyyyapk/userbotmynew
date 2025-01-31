import os
from loads import Data, Description

def handling_plugins():
    try:
        folders = os.listdir('plugins')

        for folder in folders:
            init_file = os.path.join('plugins', folder, '__init__.py')
            if os.path.exists(init_file):
                md = __import__('plugins.' + folder + '.__init__')

                if hasattr(dict(md.__dict__.items())[folder], '__description__'):
                    if not isinstance(dict(md.__dict__.items())[folder].__description__, Description):
                        print(f'\033[41mОшибка в плагине {folder}: Описание не корректное\033[0m')
                        continue
                    
                    Data.description.update({folder: dict(md.__dict__.items())[folder].__description__})
    except Exception as e:
        print(e)

def handle_plugin(pack_name: str):
    try:
        md = __import__('pluging.' + pack_name + '.__init__.py')

        if hasattr(dict(md.__dict__.items())[pack_name], '__description__'):
            if not isinstance(dict(md.__dict__.items())[pack_name].__description__, Description):
                print(f'\033[41mОшибка в плагине {pack_name}: Описание не корректное\033[0m')
                return
            
            Data.description.update({pack_name: dict(md.__dict__.items())[pack_name].__description__})
    except Exception as e:
        print(e)