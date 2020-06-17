import os
from .common import template
from .file import open_file_from_template_dir, write_file, get_path_from_template_dir
from ..const import TARGET_FILE_FIELD, TARGET_METHOD_FIELD, TARGET_METHOD_RETURN_FIELD, TARGET_ASSET_LIST, TARGET_VARIABLE_INITIALIZATIONS
from ..logger import info, error, jump
from colored import fg, attr
from shutil import copyfile

class LanguageGenerator():

    def __init__(self, language, answers):
        self._language = language
        self._root = answers['name']
        self._answers = answers

    def create(self):
        jump()
        info('Creating ' + self._language.type + ' challenge in ' + fg(208) + './' + self._root + '.')
        jump()
        self.create_folders()
        self.append_assets_to_answers()
        self.append_variable_initalizations_to_answers()
        self.generate_challenge_yaml()
        self.generate_template_file()
        self.generate_success_file()
        self.generate_solve_file()
        self.generate_run_file()
        self.generate_docs()
        self.copy_common_files()
        self.copy_assets()

        info('Challenge ' + self._root + ' created with success!')

    def append_variable_initalizations_to_answers(self):
        self._answers[TARGET_VARIABLE_INITIALIZATIONS] = []
        for var in self._language.variable_initializations:
            if var.type == self._answers[TARGET_METHOD_RETURN_FIELD]:
                self._answers[TARGET_VARIABLE_INITIALIZATIONS].append(var)

    def append_assets_to_answers(self):
        self._answers[TARGET_ASSET_LIST] = []
        for asset in self._language.newAssets:
            self._answers[TARGET_ASSET_LIST].append(asset)
    
    def copy_assets(self):
        for path in self._language.assetPaths:
            self.template_and_copy_file(path)
        for asset in self._language.newAssets:
            write_file(f'{self._root}/{asset.path}/{asset.fileName}.{asset.extension}', asset.content)

    def generate_challenge_yaml(self):
        self.template_and_copy_file('/challenge.yaml')

    def copy_common_files(self):
        self.copy_file('Dockerfile')
        self.copy_file('run.sh')
        self.copy_file('thumbnail.png')

    def template_and_copy_file(self, file):
        write_file(
            self._root + '/' + file,
            template(self._answers, open_file_from_template_dir(self._language.type, file))
        )

    def copy_file(self, file):
        copyfile(get_path_from_template_dir(self._language.type, file), self._root + '/' + file)


    def create_folders(self):
        os.makedirs(self._root + '/docs/fr', exist_ok=True)
        os.makedirs(self._root + self._language.appDirPath, exist_ok=True)
        os.makedirs(self._root + self._language.templateDirPath, exist_ok=True)
        os.makedirs(self._root + self._language.successDirPath, exist_ok=True)

    def generate_template_file(self):
        fileName = self.get_target_file_path(self._language.templateDirPath, self.get_target_file_name())
        write_file(fileName, template(self._answers, open_file_from_template_dir(self._language.type, self._language.get_path_to_template_target_file())))


    def generate_success_file(self):
        fileName = self.get_target_file_path(self._language.successDirPath, self.get_target_file_name())
        write_file(fileName, template(self._answers, open_file_from_template_dir(self._language.type, self._language.get_path_to_success_target_file())))


    def generate_solve_file(self):
        fileName = self._root + self._language.solvePath
        write_file(fileName, template(self._answers, open_file_from_template_dir(self._language.type, self._language.solvePath)))


    def generate_run_file(self):
        fileName = self._root + self._language.runPath
        write_file(fileName, template(self._answers, open_file_from_template_dir(self._language.type, self._language.runPath)))

    def generate_docs(self):
        self.template_and_copy_file('/docs/briefing.md')
        self.template_and_copy_file('/docs/fr/briefing.md')

    def get_target_file_path(self, path, file):
        return self._root + path + '/' + file + '.' + self._language.extension

    def get_target_file_name(self):
        if TARGET_FILE_FIELD in self._answers:
            return self._answers[TARGET_FILE_FIELD]
        return self._language.targetFile
