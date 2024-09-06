export const useStringUtils = () => {
  function sprintf(format: string, ...args: unknown[]): string {
    let i = 0;
    return format.replace(/%[sd]/g, function (match) {
      if (i >= args.length) {
        // If there are not enough arguments, return the placeholder as is
        return match;
      }

      if (match === '%s') {
        return String(args[i++]);
      } else if (match === '%d') {
        const arg = args[i++];
        if (typeof arg !== 'number' || isNaN(arg)) {
          // Handle the case where the argument is not a valid number
          throw new Error('Expected a number for %d placeholder');
        }
        return arg.toString();
      }
      return match;
    });
  }

  function nullIfEmpty(str: string) {
    return str === '' ? null : str;
  }

  function undefinedIfEmpty(str: string) {
    return str === '' ? undefined : str;
  }

  function updateValueIfTextNotInMatch<T, R>(
    input: T,
    field1: string,
    match: string | string[],
    returnValue: R
  ): T | R {
    if (typeof match === 'string') {
      match = [match];
    }

    return match.includes(field1) ? input : returnValue;
  }

  function isValidEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  // Function to get the text by value
  function getTextByValue(
    value: number | string,
    array: Array<{ [key: string | number]: string | number }>
  ): string | number | undefined {
    const result = array.find((option) => option.value === value);
    return result?.text;
  }

  function deplural(text: string, ifTrue = true): string {
    if (!ifTrue) {
      return text;
    }
    if (text.endsWith('ies')) {
      return text.slice(0, -3) + 'y'; // e.g., 'cities' -> 'city'
    }
    if (text.endsWith('es')) {
      return text.slice(0, -2); // e.g., 'buses' -> 'bus'
    }
    if (text.endsWith('s')) {
      return text.slice(0, -1); // e.g., 'cats' -> 'cat'
    }
    return text;
  }

  function capitalise(input: string): string {
    // Regular expression to match sentence boundaries (e.g., full stops followed by whitespace or end of string)
    const sentenceEndPattern = /([.!?])(\s+|$)/g;

    // Capitalize the first letter of each sentence
    return input
      .replace(sentenceEndPattern, (match, p1, p2, offset, string) => {
        // Capitalize the letter following a sentence boundary
        const nextCharIndex = offset + match.length;
        if (nextCharIndex < string.length) {
          return match + string.charAt(nextCharIndex).toUpperCase();
        }
        return match;
      })
      .replace(/^\w/, (firstLetter) => firstLetter.toUpperCase()); // Capitalize the very first letter of the string
  }

  return {
    sprintf,
    nullIfEmpty,
    undefinedIfEmpty,
    updateValueIfTextNotInMatch,
    isValidEmail,
    getTextByValue,
    deplural,
    capitalise,
  };
};
