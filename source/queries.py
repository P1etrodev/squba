from os.path import realpath

QUERY_REPR = 'SqubaQuery'


class DeployQuery:
    """
    Provides a valid query to "deploy" functionality
    """

    def __init__(self,
                 filename: str,
                 dest: str,
                 is_dir: bool = False,
                 force: bool = False,
                 origin: str = None,  # type: ignore
                 ):
        """
        Provides a valid query to "deploy" functionality

        Args:
            filename (str): The name of the deployed file/directory
            dest (str): The destination path
            is_dir (bool, optional): Whether a directory should be created. Defaults to False.
            force (bool, optional): Whether to force file overwriting. Defaults to False.
            origin (str, optional): The path to the original file/directory (to be copied). Defaults to None.
        """
        self.filename = filename
        self.is_dir = is_dir
        self.force = force
        self.dest = dest
        self.origin = origin

    def __repr__(self):
        return QUERY_REPR


class PurgeQuery:
    """
    Provides a valid query to "purge" functionality
    """

    def __init__(self,
                 path: str = realpath('.'),
                 terms: list[str] = [],
                 extensions: list[str] = [],
                 all: bool = False,
                 ignore_terms: list[str] = [],
                 ignore_files: list[str] = [],
                 ):
        """
        Provides a valid query to "purge" functionality

        Args:
            path (str, optional): The path where to look for files with the provided terms/extensions. Defaults to current working directory.
            terms (list[str], optional): A list of terms to look for. Defaults to [ ].
            extensions (list[str], optional): A list of extensions to look. Defaults to [ ].
            all (bool, optional): Delete all files in the provided path. Defaults to False.
            ignore_terms (list[str], optional): A list of terms to ignore. Defaults to [ ].
            ignore_files (list[str], optional): A list of files to ignore. Defaults to [ ].
        """
        self.path = path,
        self.terms = terms,
        self.extensions = extensions,
        self.all = all,
        self.ignore_terms = ignore_terms,
        self.ignore_files = ignore_files

    def __repr__(self):
        return QUERY_REPR


class PopulateQuery:
    """Provides a valid query to "populate" functionality"""

    def __init__(self,
                 dest: str = realpath('.'),
                 files: list[str] = []
                 ):
        """
        Provides a valid query to "populate" functionality

        Args:
            files (list[str], optional): A list of files to create like "file.txt*5" where 5 is the amount of files, you can also add % to indicate that the provided name will be created as a directory like "%Folder*5". Defaults to [].
            dest (str, optional): Where to create the files. Defaults to current working directory.
        """
        self.files = files
        self.dest = dest

    def __repr__(self):
        return QUERY_REPR
