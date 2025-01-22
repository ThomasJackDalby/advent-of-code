// Advent Of Code 2020 - Puzzle 2
// https://adventofcode.com/2024/day/1
// Tom Dalby - https://github.com/thomasjackdalby
// Date: 2024-02-15 10:59:00

const string inputFilePath = "input.txt";

static PasswordRule[] loadFile(string filePath)
{
    static PasswordRule parseLine(string line)
    {
        string[] parts = line.Split(':');
        string[] rule = parts[0].Split(" ");
        string[] values = rule[0].Split("-");
        int min = Int32.Parse(values[0]);
        int max = Int32.Parse(values[1]);
        char letter = rule[1][0];
        string input = parts[1].Trim();
        return new(min, max, letter, input);
    }

    using Stream stream = File.OpenRead(inputFilePath);
    using StreamReader reader = new(stream);
    return reader.ReadToEnd()
        .Split("\n")
        .Select(parseLine)
        .ToArray();
}

static void solvePart1(PasswordRule[] data)
{
    int numberOfValidPasswords = 0;
    foreach (PasswordRule rule in data)
    {
        int count = rule.Input.Count(c => c == rule.Letter);
        if (count >= rule.Min && count <= rule.Max) numberOfValidPasswords++;
    }
    Console.WriteLine($"Part 1: {numberOfValidPasswords}");
}

static void solvePart2(PasswordRule[] data)
{
    int numberOfValidPasswords = 0;
    foreach (PasswordRule rule in data)
    {
        if ((rule.Input[rule.Min - 1] == rule.Letter) != (rule.Input[rule.Max - 1] == rule.Letter)) numberOfValidPasswords++;
    }
    Console.WriteLine($"Part 1: {numberOfValidPasswords}");
}

PasswordRule[] rules = loadFile("input.txt");
solvePart1(rules);
solvePart2(rules);

record struct PasswordRule(int Min, int Max, char Letter, string Input);