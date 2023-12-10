namespace AdventOfCode2023.Extensions;

public static class StringExtensions
{
    public static string RemoveSuffix(this string s, string suffix)
    {
        if (s.EndsWith(suffix))
        {
            return s[..^suffix.Length];
        }

        return s;
    }

    public static string Multiply(this string s, int n)
    {
        return string.Concat(Enumerable.Repeat(s, n));
    }
}
