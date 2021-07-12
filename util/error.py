
class DirectoryNotFoundError(Exception):
    "指定されたディレクトリが存在しなかった時に投げるエラー"


class DirectoryAlreadyExistsError(Exception):
    """指定されたディレクトリが既に存在する時に投げるエラー"""


class DotenvKeyNotFoundError(Exception):
    """.envファイルに指定されたキーが存在しない時に投げるエラー"""
