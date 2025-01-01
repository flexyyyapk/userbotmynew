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
                
                if hasattr(dict(md.__dict__.items())[folder], '__modules__'):
                    if not isinstance(dict(md.__dict__.items())[folder].__modules__, list):
                        print(f'\033[41mОшибка в плагине {folder}: Неверный список модулей\033[0m')
                        continue
                    Data.modules.extend(dict(md.__dict__.items())[folder].__modules__)
    except ImportError as e:
        pass
