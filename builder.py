import shutil
import os
from util import *


def build(dirname: str = "env") -> None:
    """実行環境の生成を行う
    WARN: Macは対応してません(使わないので)

    Args:
        dirname (string): 生成先のディレクトリ. デフォルトはenv/.

    Raises:
        DirectoryNotFoundError: 実行環境の生成に必要なディレクトリが存在しない時に投げられるエラー
        DirectoryAlreadyExistsError: 実行環境が既に生成されていると投げられます
    """

    # TODO: .envなどに切り出す
    __basedir = "./FTG4.50"

    print("FTGの実行環境の生成を行います.")

    if not os.path.exists(__basedir):
        raise DirectoryNotFoundError("FTG4.50が指定の位置に配置されていません.")

    if os.path.exists(dirname):
        raise DirectoryAlreadyExistsError("実行環境の生成が既に行われています.")

    os.mkdir(dirname)

    # TODO: 例外処理を書く
    shutil.copytree(__basedir + "/lib", "{}/lib".format(dirname))
    shutil.copytree(__basedir + "/data", "{}/data".format(dirname))
    shutil.copytree(__basedir + "/log", "{}/log".format(dirname))
    shutil.copy(__basedir + "/FightingICE.jar",
                "{}/FightingICE.jar".format(dirname))

    print("実行環境の生成に成功しました")
    print("生成先は{}です".format(dirname))


def clean(dirname: str = "env") -> None:
    """生成されている実行環境を削除する

    Args:
        dirname (string): 実行環境のディレクトリ. デフォルトはenv/.
    """
    print("実行環境の削除を行います.")

    print("実行環境の削除を行いました.")
    shutil.rmtree(dirname)
    print("削除したディレクトリは{}です.".format(dirname))


if __name__ == "__main__":
    build()
    # clean()
