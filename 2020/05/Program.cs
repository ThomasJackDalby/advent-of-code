// Advent Of Code 2020 - Puzzle 5
// https://adventofcode.com/2020/day/5
// Tom Dalby - https://github.com/thomasjackdalby
// Date: 01/03/2024 11:36:07

const string DefaultInputFilePath = "input.txt";

// --- Solution Start ----

string[] LoadInputFile(string filePath)
{
    if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
    using Stream stream = File.Open(filePath, FileMode.Open, FileAccess.Read);
    using StreamReader reader = new(stream);
    return reader.ReadToEnd().Split("\n");
}

static (int Row, int Column) ParseBoardingPass(string input)
{
    static (int, int) split((int Min, int Max) input, bool firstHalf)
    {
        int mid = input.Min + (input.Max - input.Min) / 2;
        if (firstHalf) return (input.Min, mid);
        else return (mid+1, input.Max);
    }
    static int reduce(string input, Predicate<char> selector)
    {
        Console.WriteLine("---------");
        (int Min, int Max) range = (0, (int)Math.Pow(2, input.Length));
        foreach (char c in input)
        {
            Console.WriteLine($"{range} [{c}]");
            range = split(range, selector(c));
        }
        Console.WriteLine($"{range}");
        if (range.Min != range.Max) throw new Exception($"{range}");
        return range.Min;
    }

    Console.WriteLine($"--{input}--");
    int row = reduce(input[..7], c => c == 'F');
    int column = reduce(input[8..], c => c == 'L');
    return (row, column);
}

static int ConvertToSeatID(int row, int column) => row * 8 + column;

int SolvePart1(string[] data)
{
    return data
        .Select(boardingPass => ParseBoardingPass(boardingPass))
        .Select(coord => ConvertToSeatID(coord.Row, coord.Column))
        .Max();
}

int SolvePart2(string[] data)
{
    int result = -1;
    return result;
}

// --- Solution End ----

string inputFilePath = args.Length >= 2
    ? args[1]
    : DefaultInputFilePath;
Console.WriteLine($"Loading [{inputFilePath}]");
 
string[] data = LoadInputFile(inputFilePath);
Console.WriteLine($"Part 1: {SolvePart1(data)}");
Console.WriteLine($"Part 2: {SolvePart2(data)}");