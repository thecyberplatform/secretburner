import secrets
import string


class RandomStringGenerator:
    def __init__(
        self,
        length: int,
        include_alpha: bool = True,
        include_numeric: bool = True,
        include_symbols: bool = False,
    ):
        """
        Initializes the RandomStringGenerator with specific properties for generating random strings.

        Parameters:
            length (int): The desired length of the generated random string.
            include_alpha (bool): Indicates if alphabetic characters should be included. Defaults to True.
            include_numeric (bool): Indicates if numeric characters should be included. Defaults to True.
            include_symbols (bool): Indicates if symbol characters should be included. Defaults to False.

        Description:
            This constructor sets up the generator with options to include alphabetic, numeric, and symbol characters.
            It calls `_build_character_set` to create a string of possible characters based on these options.
        """
        self.length = length
        self.include_alpha = include_alpha
        self.include_numeric = include_numeric
        self.include_symbols = include_symbols
        self.characters = self._build_character_set()

    def _build_character_set(self) -> str:
        """
        Builds a string of characters that will be used to generate random strings.

        Returns:
            str: A string containing all characters that can be used in the random string generation.

        Description:
            This method aggregates characters from alphabetic, numeric, and symbol sets based on the instance
            configuration. It raises an error if no character types are included, ensuring that there is
            always a valid set of characters to use for string generation.
        """
        characters = ""
        if self.include_alpha:
            characters += (
                string.ascii_letters
            )  # Adds both lowercase and uppercase alphabetic characters
        if self.include_numeric:
            characters += string.digits  # Adds numeric characters
        if self.include_symbols:
            characters += string.punctuation  # Adds symbols

        if not characters:
            raise ValueError(
                "At least one character type must be included (alpha, numeric, or symbols)."
            )

        return characters

    def generate(self) -> str:
        """
        Generates a cryptographically secure random string using the character set built by `_build_character_set`.

        Returns:
            str: A random string of the specified length and character composition.

        Description:
            This method uses the `secrets.choice` function to ensure that the random selection of characters
            is suitable for security-sensitive applications. It generates a string of the desired length by
            repeatedly choosing random characters from the pre-defined set.
        """
        return "".join(secrets.choice(self.characters) for _ in range(self.length))
