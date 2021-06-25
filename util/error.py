
class DirectoryNotFoundError(Exception):
    "指定されたディレクトリが存在しなかった時に投げるエラー"


class DirectoryAlreadyExistsError(Exception):
    """指定されたディレクトリが既に存在する時に投げるエラー"""
