// Advent Of Code 2020 - Puzzle 4
// https://adventofcode.com/2020/day/4
// Tom Dalby - https://github.com/thomasjackdalby
// Date: 26/02/2024 07:23:26

using System.Linq;

const string DefaultInputFilePath = "input.txt";

// --- Solution Start ----

Dictionary<string, string>[] LoadInputFile(string filePath)
{
    if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
    using Stream stream = File.Open(filePath, FileMode.Open, FileAccess.Read);
    using StreamReader reader = new(stream);
    return reader.ReadToEnd()
        .Split("\r\n\r\n")
        .Select(lines => lines.Split("\r\n")
            .SelectMany(line => line.Split(" "))
            .Select(data => data.Split(":"))
            .ToDictionary(data => data[0], data => data[1]))
        .ToArray();
}

int SolvePart1(Dictionary<string, string>[] data)
{
    return data.Where(passport =>
        {
            return passport.ContainsKey("byr")
            && passport.ContainsKey("iyr")
            && passport.ContainsKey("eyr")
            && passport.ContainsKey("hgt")
            && passport.ContainsKey("hcl")
            && passport.ContainsKey("ecl")
            && passport.ContainsKey("pid");
        }).Count();
}

int SolvePart2(Dictionary<string, string>[] data)
{
    List<Func<Dictionary<string, string>, bool>> rules = new();
    void register(string key, Func<string, bool> validator)
    {
        rules.Add(data =>
        {
            if (!data.TryGetValue(key, out string? value)) return false;
            bool result = validator(value);
            Console.WriteLine($"{key} : {value} [{result}]");
            return result;
        });
    }
    void registerInt(string key, int min, int max) => register(key, value =>
    {
        if (!Int32.TryParse(value, out int result)) return false;
        return result >= min && result <= max;
    });

    registerInt("byr", 1920, 2002);
    registerInt("iyr", 2010, 2020);
    registerInt("eyr", 2020, 2030);
    register("hgt", value =>
    {
        if (value.Length < 3) return false;
        if (!Int32.TryParse(value[..^2], out int result)) return false;
        if (value[^2..] == "cm") return result >= 150 && result <= 193;
        if (value[^2..] == "in") return result >= 59 && result <= 76;
        return false;
    });
    register("hcl", value =>
    {
        if (value.Length != 7) return false;
        if (value[0] != '#') return false;
        return value.Skip(1).All(c => (c >= 'a' && c <= 'f')
        || (c >= 'A' && c <= 'F')
        || (c >= '0' && c <= '9'));
    });
    HashSet<string> colours = new(new[]
    {
        "amb",
        "blu",
        "brn",
        "gry",
        "grn",
        "hzl",
        "oth",
    });
    register("ecl", value => colours.Contains(value));
    register("pid", value => value.Length == 9 && value.All(c => Char.IsDigit(c)));

    return data.Count(passport => rules.All(rule => rule(passport)));
}

// --- Solution End ----

string inputFilePath = args.Length > 1
    ? args[1]
    : DefaultInputFilePath;
Console.WriteLine($"Loading [{inputFilePath}]");

Dictionary<string, string>[] data = LoadInputFile(inputFilePath);
Console.WriteLine($"Part 1: {SolvePart1(data)}");
Console.WriteLine($"Part 2: {SolvePart2(data)}");

public static class Extensions
{
    public static IEnumerable<T> WhereNotNull<T>(this IEnumerable<T?> self)
    {
        foreach (T? element in self)
        {
            if (element is not null) yield return element;
        }
    }
}