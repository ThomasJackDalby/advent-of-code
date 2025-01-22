// Advent Of Code 2020 - Puzzle 3
// https://adventofcode.com/2024/day/3
// Tom Dalby - https://github.com/thomasjackdalby
// Date: 2024-02-15 14:28:00

const string inputFilePath = "input.txt";

static Map loadFile(string filePath)
{
    using Stream stream = File.OpenRead(inputFilePath);
    using StreamReader reader = new(stream);

    return new Map(reader.ReadToEnd()
        .Split("\n")
        .Select(line => line.Trim().ToCharArray())
        .ToArray());
}

static void solvePart1(Map data)
{
    int result = -1;
    Console.WriteLine($"Part 1: {result}");
}

static void solvePart2(Map data)
{
    int result = -1;
    Console.WriteLine($"Part 2: {result}");
}

Map map = loadFile("input.txt");
solvePart1(map);
solvePart2(map);

record struct Map(char[][] Data);