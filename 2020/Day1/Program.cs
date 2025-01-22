// Advent Of Code 2020 - Puzzle 1
// https://adventofcode.com/2024/day/1
// Tom Dalby - https://github.com/thomasjackdalby
// Date: 2024-02-15 10:59:00

const string inputFilePath = "input.txt";

static int[] loadFile(string filePath)
{
    using Stream stream = File.OpenRead(inputFilePath);
    using StreamReader reader = new(stream);
    return reader.ReadToEnd()
        .Split("\n")
        .Select(s => Int32.Parse(s.Trim()))
        .ToArray();
}


static int solvePair(Span<int> inputs, int target)
{
    for (int i = 0; i < inputs.Length; i++)
    {
        int a = inputs[i];
        for (int j = i + 1; j < inputs.Length; j++)
        {
            int b = inputs[j];
            if (a + b != target) continue;
            Console.WriteLine($"{a}+{b}={target}");
            return a * b;
        }
    }
    return -1;
}
static int solvePart1()
{
    int[] inputs = loadFile("input.txt");
    return solvePair(inputs, 2020);
}

static int solvePart2()
{
    Span<int> inputs = loadFile("input.txt");
    for (int i = 0; i < inputs.Length; i++)
    {
        int result = solvePair(inputs[(i+1)..], 2020 - inputs[i]);
        if (result != -1) return result * inputs[i];
    }
    return -1;
}

Console.WriteLine($"Part 1: {solvePart1()}");
Console.WriteLine($"Part 2: {solvePart2()}");